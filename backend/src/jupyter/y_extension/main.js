define([
    'jquery',
    './constants',
    'base/js/namespace',
    'base/js/events',
], function ($, constants, Jupyter, events) {
    window.Jupyter = Jupyter; // debug usage
    // Copy pasted from jupyter nbclassic source
    Jupyter.CodeCell.prototype.get_text_original = function () {
        return this.code_mirror.getValue();
    };

    // Copy pasted from jupyter nbclassic source
    Jupyter.CodeCell.prototype.execute_original = function (stop_on_error) {
        if (!this.kernel) {
            console.log(i18n.msg._("Can't execute cell since kernel is not set."));
            return;
        }

        if (stop_on_error === undefined) {
            if (this.metadata !== undefined &&
                this.metadata.tags !== undefined) {
                if (this.metadata.tags.indexOf('raises-exception') !== -1) {
                    stop_on_error = false;
                } else {
                    stop_on_error = true;
                }
            } else {
                stop_on_error = true;
            }
        }

        this.clear_output(false, true);
        var old_msg_id = this.last_msg_id;
        if (old_msg_id) {
            this.kernel.clear_callbacks_for_msg(old_msg_id);
            delete Jupyter.CodeCell.msg_cells[old_msg_id];
            this.last_msg_id = null;
        }
        if (this.get_text().trim().length === 0) {
            // nothing to do
            this.set_input_prompt(null);
            return;
        }
        this.set_input_prompt('*');
        this.element.addClass("running");
        var callbacks = this.get_callbacks();

        this.last_msg_id = this.kernel.execute(this.get_text(), callbacks, {
            silent: false, store_history: true,
            stop_on_error: stop_on_error
        });
        Jupyter.CodeCell.msg_cells[this.last_msg_id] = this;
        this.render();
        this.events.trigger('execute.CodeCell', { cell: this });
        var that = this;
        function handleFinished(evt, data) {
            if (that.kernel.id === data.kernel.id && that.last_msg_id === data.msg_id) {
                that.events.trigger('finished_execute.CodeCell', { cell: that });
                that.events.off('finished_iopub.Kernel', handleFinished);
            }
        }
        this.events.on('finished_iopub.Kernel', handleFinished);
    };

    function blobToBase64(blob) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            reader.onloadend = function () {
                resolve(reader.result);
            };
        });
    };

    function get_cell_by_id(cell_id) {
        var all_cells = Jupyter.notebook.get_cells();
        var this_cell = null;

        for(var i = 0; i < all_cells.length; ++i) {
            if(all_cells[i].cell_id == cell_id) {
                this_cell = all_cells[i];
                break;
            }
        }
        return this_cell;
    };


    function setupCustomMessageListener() {
        Jupyter.notebook.kernel.comm_manager.register_target('custom_message', function(comm, msg) {
            // Handle the custom message data here
            console.log("Received custom message:", msg);

            // The actual data sent from the kernel will be in msg.content.data
            var dataFromKernel = msg.content.data;
            // Process the data as needed...
            var new_cell = Jupyter.notebook.insert_cell_below('code');
            new_cell.set_text(dataFromKernel);
            

            console.log(dataFromKernel)
            // register callback
            // comm.on_msg(handle_msg)

        });

        Jupyter.notebook.kernel.comm_manager.register_target('custom_insert_cell', function(comm, msg) {
            console.log("Received custom message:", msg);
            var data_from_kernel = msg.content.data;
            switch (data_from_kernel.type) {
                case "ds_upload_file":
                    new_cell = insert_yorg_cell(constants.OPTION_DS_UPLOAD_FILE);
                    break;
                case "ds_query":
                    new_cell = insert_yorg_cell(constants.OPTION_DS_QUERY);
                    new_cell.execute();
                    break;
                case "ds_code":
                    new_cell = insert_yorg_cell(constants.OPTION_DS_CODE);
                    new_cell.set_text(data_from_kernel.code);
                    break;
                case "auto_refresh":
                    new_cell = insert_yorg_cell(constants.OPTION_AUTO_REFRESH, 'bottom');
                    new_cell.set_text("# nothing to do");
                    new_cell.execute();
                    Jupyter.notebook.delete_cell(Jupyter.notebook.get_cells().length - 1);
                    break;
                default:
                    break;
            }
        });



        Jupyter.notebook.kernel.comm_manager.register_target('custom_get_output', function(comm, msg) {
            console.log("Received custom message:", msg);
            var data_from_kernel = msg.content.data;
            
            // if cell_id is null, send all cells' output
            if (data_from_kernel.cell_id == null) {
                var all_data = [];
                for (var i = 0; i < Jupyter.notebook.get_cells().length; ++i) {
                    var this_cell = Jupyter.notebook.get_cell(i);
                    var data = {
                        cell_id: this_cell.cell_id,
                        outputs: this_cell.output_area.outputs,
                    }
                    all_data.push(data);
                }
                var comm = Jupyter.notebook.kernel.comm_manager.new_comm("custom_all_cell_output", all_data);
                comm.close();
                return;
            }

            var this_cell = get_cell_by_id(data_from_kernel.cell_id);
            var data = {
                cell_id: data_from_kernel.cell_id,
                outputs: this_cell.output_area.outputs,
            }            

            var comm = Jupyter.notebook.kernel.comm_manager.new_comm("custom_cell_output", data);
            comm.close();
        });

        

        Jupyter.notebook.kernel.comm_manager.register_target('custom_set_text', function(comm, msg) {
            console.log("Received custom message:", msg);
            var data_from_kernel = msg.content.data;
            
            var cell_id = data_from_kernel.cell_id;
            var text = data_from_kernel.text;
            var operation = data_from_kernel.operation;

            var all_cells = Jupyter.notebook.get_cells();
            var this_cell = null;

            for(var i = 0; i < all_cells.length; ++i) {
                if(all_cells[i].cell_id == cell_id) {
                    this_cell = all_cells[i];
                    break;
                }
            }

            if(this_cell == null) {
                console.log("custom_set_text: Cannot find cell which id is " + cell_id);
                return;
            }

            switch (operation) {
                case "set":
                    this_cell.set_text(text);
                    break;
                case "append":
                    original_text = this_cell.get_text();
                    if (original_text != "") {
                        this_cell.set_text(original_text + '\n' + text);
                    } else {
                        this_cell.set_text(text);
                    }
                    break;
                case "clear":
                    this_cell.set_text("");
                default:
                    break;
            }
        });

        Jupyter.notebook.kernel.comm_manager.register_target('')
    }

    var get_input_prefix = function (yorg_cell_type) {
        switch (yorg_cell_type) {
            case constants.OPTION_SWE:
                return 'SWE In';
            case constants.OPTION_GPT:
                return 'GPT In';
            case constants.OPTION_PYTHON:
                return 'In';
            case constants.OPTION_DATA_ANALYSIS:
                return 'DS In';
            case constants.OPTION_DS_CODE:
                return 'DS In';
            case constants.OPTION_DS_QUERY:
                return 'DS In';
            case constants.OPTION_DS_UPLOAD_FILE:
                return 'DS In';
        }
        return 'In';
    }

    var yorg_input_prompt_function = function (prompt_value, lines_number, prefix) {
        var ns;
        if (prompt_value === undefined || prompt_value === null) {
            ns = "&nbsp;";
        } else {
            ns = encodeURIComponent(prompt_value);
        }
        return '<bdi>' + prefix + '</bdi>&nbsp;[' + ns + ']:';
    };

    var insert_yorg_cell = function (type = constants.OPTION_SWE, position = 'below') {

        var new_cell;
        switch (position) {
            case 'below':
                new_cell = Jupyter.notebook.insert_cell_below('code');
                break;
            case 'above':
                new_cell = Jupyter.notebook.insert_cell_above('code');
                break;
            case 'bottom':
                new_cell = Jupyter.notebook.insert_cell_at_bottom('code');
                break;
            default:
                new_cell = Jupyter.notebook.insert_cell_below('code');
                break;
        }
            
        Jupyter.notebook.select_next();
        new_cell._metadata.yorg_cell = true;
        new_cell._metadata.yorg_cell_type = type;

        // reset input prompt
        new_cell.set_input_prompt = function (number) {
            var nline = 1;
            if (this.code_mirror !== undefined) {
                nline = this.code_mirror.lineCount();
            }
            this.input_prompt_number = number;
            var prompt_html = yorg_input_prompt_function(this.input_prompt_number, nline, get_input_prefix(this._metadata.yorg_cell_type));

            // This HTML call is okay because the user contents are escaped.
            this.element.find('div.input_prompt').html(prompt_html);
            this.events.trigger('set_dirty.Notebook', { value: true });
        };
        new_cell.set_input_prompt();

        new_cell.execute = function (stop_on_error) {
            this.get_text = function () {
                var original_text = this.get_text_original();
                var data = {
                    type: this._metadata.yorg_cell_type,
                    cell_id: this.cell_id,
                    code: original_text,
                };
                if (this._metadata.yorg_upload_files) {
                    data.yorg_upload_files = this._metadata.yorg_upload_files;
                }
                return JSON.stringify(data)
            }
            this.execute_original(stop_on_error);
            this.get_text = this.get_text_original;
        } 

        switch (type) {
            case constants.OPTION_SWE: {
                new_cell.execute();
                // disable SWE cell execute function
                new_cell.execute = function (stop_on_error) { };
                // change SWE cell style

                new_cell.set_text('"💡 Software engineer agent is running, please interact with it in the output area."')
                new_cell.metadata.editable = false;
                new_cell.is_deletable = function () { return true; };
                break;
            }

            case constants.OPTION_DS_UPLOAD_FILE: {
                new_cell.set_text('"📁 Upload your files here."');
                new_cell._metadata.yorg_upload_files = []
                var input = document.createElement('input');

                file_name = ''                

                input.type = 'file';
                input.onchange = async function() {
                    for (const file of this.files) {
                        const res = await blobToBase64(file)
                        new_cell._metadata.yorg_upload_files.push({
                            name: file.name,
                            size: file.size,
                            type: file.type,
                            content: res,
                        })
                    }
                    new_cell.execute();
                    // disable file upload cell execute function
                    new_cell.execute = function (stop_on_error) { };
                    // Do something with the file.
                };
                input.click();

                // change File Upload cell style
                new_cell._metadata.editable = false;
                new_cell.is_deletable = function () { return true; };
                break;
            }

            case constants.OPTION_DATA_ANALYSIS: {
                new_cell.execute();
                // disable DS cell execute function
                new_cell.execute = function (stop_on_error) { };
                // change DS cell style
                new_cell.set_text("\"🤔 I'm your custom data scientist agent. Please choose your option:\"");
                new_cell._metadata.editable = false;
                new_cell.is_deletable = function () { return true; };
                break;
            }

            case constants.OPTION_DS_QUERY: {
                new_cell.set_text('"🔍 Please input your query here."');
                break;
            }

            default:
                break;
        }
        return new_cell;
    };

    function registerYorgButton() {
        var menuOpen = false;
        var $menu = $('<div/>')
            .attr('id', 'yorg_type')
            .attr('role', 'combobox')
            .addClass('dropdown-menu').addClass('hidden')
            .append(
                $('<li />').append($('<a />').text('Sofware Engineer').on('click', () => insert_yorg_cell(constants.OPTION_SWE)))
            )
            .append(
                $('<li />').append($('<a />').text('OpenAI Chat').on('click', () => insert_yorg_cell(constants.OPTION_GPT)))
            )
            .append(
                $('<li />').append($('<a />').text('Python Code').on('click', () => insert_yorg_cell(constants.OPTION_PYTHON)))
            )
            .append(
                $('<li />').append($('<a />').text('File Upload').on('click', () => insert_yorg_cell(constants.OPTION_FILE_UPLOAD)))
            )
            .append(
                $('<li />').append($('<a />').text('Data Analysis').on('click', () => insert_yorg_cell(constants.OPTION_DATA_ANALYSIS)))
            )
        function toggleMenu() {
            menuOpen = !menuOpen;
            if (menuOpen) {
                $btn.addClass('open');
                $menu.removeClass('hidden');
            } else {
                $btn.removeClass('open');
                $menu.addClass('hidden');
            }
        }

        var $btn = $(Jupyter.toolbar.add_buttons_group([
            Jupyter.keyboard_manager.actions.register({
                'help': 'Create a cell to interact with agents!',
                'icon': 'fa-plus',
                'handler': toggleMenu,
            }, 'YORG', 'add-yorg-cell'),
        ])).find('.btn').attr('id', constants.ADD_YORG_CELL_ID).attr('class', 'dropdown');

        $btn.append($menu);
    }

    function removeCustomButton() {
        // Check if the button with the specified ID exists.
        var buttonElement = $('#' + constants.ADD_YORG_CELL_ID);
        if (buttonElement.length) {
            buttonElement.remove();
        }
    }

    // Run on start
    function load_ipython_extension() {
        console.log('================= Extension loaded =================')
        Jupyter.notebook.events.on(constants.KERNEL_READY_ENAME, function () {
            if (Jupyter.notebook.kernel.name === constants.YORG_KERNEL_NAME) {
                setupCustomMessageListener();
                Jupyter.CodeCell.prototype.execute = function (stop_on_error) {
                    Jupyter.CodeCell.prototype.get_text = function () {
                        var original_text = this.get_text_original();
                        return JSON.stringify({
                            type: 'python',
                            cell_id: this.cell_id,
                            code: original_text,
                        })
                    }
                    this.execute_original(stop_on_error);
                    Jupyter.CodeCell.prototype.get_text = this.get_text_original;
                }
                registerYorgButton();
            } else {
                removeCustomButton();
            }
        })
    }
    return {
        load_ipython_extension: load_ipython_extension
    };
});
