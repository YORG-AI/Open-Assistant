from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.google.google_sheets.google_sheets_model import (
    CreateDocumentInput, DeleteDocumentInput, AppendOrUpdateInput, ClearSheetInput,
    CreateSheetInput, DeleteColumnsOrRowsInput, ReadRowsInput, RemoveSheetInput,
    UpdateRowsInput
)
from src.utils.router_generator import generate_node_end_points

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json
import os

google_sheets_node_config = {
    "name": "google_sheets",
    "description": "A node that interacts with Google Sheets.",
    "functions": {
        "create_document": "Create a new Google Sheets document.",
        "delete_document": "Delete an existing Google Sheets document.",
        "append_or_update": "Append or update a row in a Google Sheets document.",
        "clear_sheet": "Clear all data from a sheet in a Google Sheets document.",
        "create_sheet": "Create a new sheet in a Google Sheets document.",
        "delete_columns_or_rows": "Delete columns or rows in a Google Sheets document.",
        "read_rows": "Read all rows from a sheet in a Google Sheets document.",
        "remove_sheet": "Remove a sheet from a Google Sheets document.",
        "update_rows": "Update all rows in a sheet in a Google Sheets document.",
    }
}

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'  # Necessary for deleting documents
]

@generate_node_end_points
class GoogleSheetsNode(BaseNode):
    config: NodeConfig = NodeConfig(**google_sheets_node_config)

    def __init__(self):
        super().__init__()
        self.credentials = self._get_credentials()
        self.service = self._get_service()

    def _get_credentials(self):
        with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as f:
            service_account_info = json.load(f)
        return Credentials.from_service_account_info(service_account_info)

    def _get_service(self):
        return build('sheets', 'v4', credentials=self.credentials)

    def create_document(self, input: CreateDocumentInput):
        drive_service = build('drive', 'v3', credentials=self.credentials)
        file_metadata = {
            'name': input.title,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        try:
            file = drive_service.files().create(body=file_metadata, fields='id').execute()
            return {"status": "success", "document_id": file.get('id')}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def delete_document(self, input: DeleteDocumentInput):
        drive_service = build('drive', 'v3', credentials=self.credentials)
        try:
            drive_service.files().delete(fileId=input.document_id).execute()
            return {"status": "success", "message": f"Document {input.document_id} deleted successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}


    def append_or_update(self, input: AppendOrUpdateInput):
        sheet_service = self.service.spreadsheets()

        # Check if the row exists based on a primary key (e.g., an ID)
        # This is just a placeholder logic. You can modify it as needed.
        range_name = f"{input.sheet_name}!A1:Z1000"  # Adjust the range accordingly
        result = sheet_service.values().get(spreadsheetId=input.document_id, range=range_name).execute()
        values = result.get('values', [])

        # Find if the entry already exists
        row_to_update = None
        for i, row in enumerate(values):
            if row and row[0] == input.primary_key:  # Assuming the first column is the primary key
                row_to_update = i
                break

        # Update or append
        if row_to_update is not None:
            # Update the existing row
            update_range = f"{input.sheet_name}!A{row_to_update + 1}"
            body = {
                'values': [input.data]  # Assuming input.data is a list of values for the row
            }
            sheet_service.values().update(spreadsheetId=input.document_id, range=update_range, valueInputOption="RAW", body=body).execute()
            return {"status": "success", "message": "Row updated successfully."}
        else:
            # Append a new row
            append_range = f"{input.sheet_name}"
            body = {
                'values': [input.data]
            }
            sheet_service.values().append(spreadsheetId=input.document_id, range=append_range, valueInputOption="RAW", body=body).execute()
            return {"status": "success", "message": "Row appended successfully."}

    def clear_sheet(self, input: ClearSheetInput):
        sheet_service = self.service.spreadsheets()

        # Clear the entire sheet
        range_name = f"{input.sheet_name}"  # This refers to the entire sheet
        try:
            sheet_service.values().clear(spreadsheetId=input.document_id, range=range_name).execute()
            return {"status": "success", "message": "Sheet cleared successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}


    def create_sheet(self, input: CreateSheetInput):
        sheet_service = self.service.spreadsheets()

        # Create a new sheet
        sheet_properties = {
            "properties": {
                "title": input.sheet_name
            }
        }
        body = {
            "requests": [
                {
                    "addSheet": sheet_properties
                }
            ]
        }

        try:
            response = sheet_service.batchUpdate(spreadsheetId=input.document_id, body=body).execute()
            new_sheet_id = response["replies"][0]["addSheet"]["properties"]["sheetId"]
            return {"status": "success", "sheet_id": new_sheet_id}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_columns_or_rows(self, input: DeleteColumnsOrRowsInput):
        sheet_service = self.service.spreadsheets()

        if input.type == "ROWS":
            range_ = {
                "sheetId": input.sheet_id,
                "dimension": "ROWS",
                "startIndex": input.start_index,
                "endIndex": input.end_index
            }
        elif input.type == "COLUMNS":
            range_ = {
                "sheetId": input.sheet_id,
                "dimension": "COLUMNS",
                "startIndex": input.start_index,
                "endIndex": input.end_index
            }
        else:
            return {"status": "error", "message": "Invalid type. Choose either 'ROWS' or 'COLUMNS'."}

        body = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": range_
                    }
                }
            ]
        }

        try:
            sheet_service.batchUpdate(spreadsheetId=input.document_id, body=body).execute()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def read_rows(self, input: ReadRowsInput):
        sheet_service = self.service.spreadsheets()

        # Constructing the range in format "SheetName!A1:D10"
        range_ = f"{input.sheet_name}!{input.range}"

        try:
            result = sheet_service.values().get(spreadsheetId=input.document_id, range=range_).execute()
            values = result.get('values', [])
            if not values:
                return {"status": "success", "data": [], "message": "No data found."}
            else:
                return {"status": "success", "data": values}
        except Exception as e:
            return {"status": "error", "message": str(e)}


    def remove_sheet(self, input: RemoveSheetInput):
        sheet_service = self.service.spreadsheets()

        # Prepare the request
        requests = [{
            "deleteSheet": {
                "sheetId": input.sheet_id
            }
        }]

        body = {
            'requests': requests
        }

        try:
            sheet_service.batchUpdate(spreadsheetId=input.document_id, body=body).execute()
            return {"status": "success", "message": "Sheet removed successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}


    def update_rows(self, input: UpdateRowsInput):
        sheet_service = self.service.spreadsheets().values()

        # Prepare the range in A1 notation format
        range_name = f"{input.sheet_name}!{input.range}"  # e.g., "Sheet1!A1:D10"

        try:
            response = sheet_service.update(
                spreadsheetId=input.document_id,
                range=range_name,
                valueInputOption="RAW",
                body={"values": input.values}
            ).execute()

            return {
                "status": "success",
                "message": f"Updated {response.get('updatedCells')} cells."
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}


