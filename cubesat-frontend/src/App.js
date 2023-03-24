import Dashboard from "./pages/Dashboard";
import TopBar from "./components/TopBar";
import { ToastContainer } from "react-toastify";
import Login from "./pages/Login";
import DashboardProvider from "./contexts/DashboardProvider";
import ApiProvider from "./contexts/ApiProvider";
import { Container } from "react-bootstrap";

export default function App() {
  return (
    <>
      <ToastContainer />
      <ApiProvider>
        <DashboardProvider>
          <Container fluid className="p-0 d-flex flex-column vh-100">
            <TopBar />
            <Dashboard />
          </Container>
          {/*<Login />*/}
        </DashboardProvider>
      </ApiProvider>
    </>
  );
}
