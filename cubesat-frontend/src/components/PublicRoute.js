import { Navigate } from "react-router-dom";
import { useUser } from "../contexts/UserProvider";

// Wraps routes that do not require the user to be logged in
// If the user is not logged in, the page is shown
// Otherwise, they are redirected to the dashboard
export default function PublicRoute({ children }) {
  const { user } = useUser();

  if (user === undefined) {
    return null;
  } else if (user) {
    return <Navigate to="/" />;
  } else {
    return children;
  }
}
