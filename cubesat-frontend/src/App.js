import Dashboard from "./pages/Dashboard";
import TopBar from "./components/TopBar";
import {ToastContainer} from 'react-toastify';
import Login from "./pages/Login";

export default function App() {
  
  return (
      <>
        <ToastContainer />
        <TopBar />
        <Dashboard />
        <Login/>
      </>
  );
}
