import { FC } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { CardMenu } from '../../commonCpns/cardMenu';
import { TopOperation } from '../../components/TopOperation';
import { AppRoutes } from '../appRouter';
import { Provider } from 'jotai';
import './index.scss';
import { ScreenProvider } from '../../components/AllFilesView/context';
const BaseStructure: FC = () => {
  return (
    <BrowserRouter>
      <Provider>
        <ScreenProvider>
          <TopOperation />

          <div className="baseStyle">
            <CardMenu />
            <AppRoutes />
          </div>
        </ScreenProvider>
      </Provider>
    </BrowserRouter>
  );
};
export default BaseStructure;
