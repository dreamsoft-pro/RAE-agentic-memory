import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";
import "./styles.css";

interface ConfigProviderProps {
  children: React.ReactNode;
}

interface ConfigContextType {
  config: Record<string, any>;
  setConfig: (key: string, val: any) => void;
  getConfig: (key: string) => any | undefined;
}

const initialState = {};

const ConfigContext = React.createContext<ConfigContextType>({
  config: initialState,
  setConfig: () => {},
  getConfig: () => undefined
});

export const ConfigProvider: React.FC<ConfigProviderProps> = ({ children }) => {
  const [config, setConfig] = useState(initialState);

  useEffect(() => {
    // Fetch initial configuration from server or API here if needed
    // Example: axios.get('/api/config').then(response => setConfig(response.data));
  }, []);

  const getConfig = (key: string) => config[key];
  const setConfigValue = (key: string, val: any) => setConfig(prevState => ({ ...prevState, [key]: val }));

  return (
    <ConfigContext.Provider value={{ config, setConfig: setConfigValue, getConfig }}>
      {children}
    </ConfigContext.Provider>
  );
};

interface PanelComponentProps {
  complexProducts?: Array<{ thickness: number }>;
}

const PanelComponent: React.FC<PanelComponentProps> = ({ complexProducts }) => {
  const [totalThickness, setTotalThickness] = useState(0);

  useEffect(() => {
    if (complexProducts) {
      const total = complexProducts.reduce((acc, product) => acc + product.thickness, 0);
      setTotalThickness(total);
    }
  }, [complexProducts]);

  return (
    <div className="flex flex-col rounded-lg shadow-md">
      {totalThickness > 0 && complexProducts?.length > 1 ? (
        <>
          <dl className="p-6 border-b bg-white rounded-t-lg">
            <dt>Total Thickness</dt>
            <dd>{`${totalThickness} mm`}</dd>
          </dl>
        </>
      ) : null}
      {totalThickness > 0 && complexProducts?.length > 1 ? (
        <div className="p-4 bg-blue-500 text-white rounded-b-lg">
          Term Realization Info
        </div>
      ) : null}
    </div>
  );
};

export default PanelComponent;