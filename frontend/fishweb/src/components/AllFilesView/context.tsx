import React, { createContext, useContext, useState } from 'react';

// 创建一个新的context
interface ScreenContextType {
  currentScreen: number;
  setCurrentScreen: React.Dispatch<React.SetStateAction<number>>;
}

const ScreenContext = createContext<ScreenContextType | undefined>(undefined);

// 创建一个Provider组件
export const ScreenProvider = ({ children }: { children: React.ReactNode }) => {
  const [currentScreen, setCurrentScreen] = useState<number>(0);

  return (
    <ScreenContext.Provider value={{ currentScreen, setCurrentScreen }}>
      {children}
    </ScreenContext.Provider>
  );
};

// 创建一个自定义hook来使用这个context
export const useScreen = (): ScreenContextType => {
  const context = useContext(ScreenContext);
  if (!context) {
    throw new Error('useScreen must be used within a ScreenProvider');
  }
  return context;
};
