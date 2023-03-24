import { createContext, useContext } from "react";
import ApiClient from "../ApiClient";

const ApiContext = createContext();

// API Context Provider
// Allows child components to share a singular instance of an API Client to make API calls
export default function ApiProvider({ children }) {
  const api = new ApiClient();

  return <ApiContext.Provider value={api}>{children}</ApiContext.Provider>;
}

export function useApi() {
  return useContext(ApiContext);
}
