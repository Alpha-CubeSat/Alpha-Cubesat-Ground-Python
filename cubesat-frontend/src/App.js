import Dashboard from "./pages/Dashboard";
import TopBar from "./components/TopBar";
import {ToastContainer} from 'react-toastify';

export default function App() {
  return (
      <>
        <ToastContainer />
        <TopBar />
        <Dashboard />
      </>
  );
}
