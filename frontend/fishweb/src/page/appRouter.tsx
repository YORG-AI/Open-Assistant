import { Navigate, useRoutes } from 'react-router-dom';
import { AllreposCardView } from './AllreposCardView';
import { ChatHistoryView } from './ChatHistoryView/ChatHistoryView';
import { CodebaseDetail } from './CodebaseDetail';
import { CodeStructureViewer } from '../components/CodeStructureViewer';
import IndvFileView from './IndvFileView';
import { DataBaseInitView } from './DataBaseInitView';
import { CodeFile } from '../components/CodeStructureViewer/codeFile';
import { SelectedRepo } from './SelectedRepo';
import { ChatHistory } from '../commonCpns/chathistory/chathistory';

function AppRoutes() {
  return useRoutes([
    {
      path: '/',
      element: <AllreposCardView />,
    },
    {
      path: '/codebase',
      element: <AllreposCardView />,
    },
    {
      path: '/codebase/detail/:id',
      element: <CodebaseDetail />,
    },
    {
      path: '/database',
      element: <AllreposCardView type="database" />,
    },
    {
      path: '/database/detail/:id',
      element: <CodebaseDetail type="database" />,
    },
    {
      path: '/chathistory',
      element: <ChatHistoryView />,
    },
    {
      path: '/codepath',
      element: <CodeStructureViewer />,
      children: [
        { path: 'codeFile', element: <CodeFile /> },
        { path: 'databastinit', element: <DataBaseInitView /> },
        { path: 'chathistory', element: <ChatHistory /> },
      ],
    },
    {
      path: '/indvfile',
      element: <IndvFileView />,
    },
    {
      path: '/repoOverview',
      element: <div>/chatOverview</div>,
    },
    {
      path: '/chat',
      element: <div>Codebase / Indv Chat / Explain Code / Half / Initial</div>,
    },
    {
      path: 'selectedRepo',
      element: <SelectedRepo />,
    },
    {
      path: '*',
      element: <Navigate to="/" />,
    },
  ]);
}
export { AppRoutes };
