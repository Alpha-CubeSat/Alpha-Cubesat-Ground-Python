import { Navigate } from "react-router-dom";
import { useUser } from "../contexts/UserProvider";

// Wraps routes that require the user to be logged in
// If the user is already logged in, the page is shown
// Otherwise, they are redirected to the login page
export default function PrivateRoute({ children }) {
  const { user } = useUser();

  if (user === undefined) {
    return null;
  } else if (user) {
    return children;
  } else {
    return <Navigate to="/login" />;
  }
}
