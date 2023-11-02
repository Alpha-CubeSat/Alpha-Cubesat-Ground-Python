import Dashboard from "./pages/Dashboard";
import TopBar from "./components/TopBar";
import { ToastContainer } from "react-toastify";
import Login from "./pages/Login";
import DashboardProvider from "./contexts/DashboardProvider";
import ApiProvider from "./contexts/ApiProvider";
import { Container } from "react-bootstrap";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import UserProvider from "./contexts/UserProvider";
import PublicRoute from "./components/PublicRoute";
import PrivateRoute from "./components/PrivateRoute";

export default function App() {
  return (
    <BrowserRouter>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar
        closeOnClick
        pauseOnFocusLoss={false}
        theme="light"
      />
      <ApiProvider>
        <UserProvider>
          <Routes>
            <Route
              path="/login"
              element={
                <PublicRoute>
                  <Login />
                </PublicRoute>
              }
            />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <DashboardProvider>
                    <Container fluid className="vh-100 p-0">
                      <TopBar />
                      <Dashboard />
                    </Container>
                  </DashboardProvider>
                </PrivateRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </UserProvider>
      </ApiProvider>
    </BrowserRouter>
  );
}
