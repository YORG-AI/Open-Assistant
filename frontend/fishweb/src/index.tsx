import React from "react";
import ReactDOM from "react-dom/client";
import "./index.scss";
import "@arco-design/web-react/dist/css/arco.css";
import reportWebVitals from "./reportWebVitals";
import BaseStructure from "./page/BaseStrcture";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
   <BaseStructure/>
  </React.StrictMode>
);

reportWebVitals();
