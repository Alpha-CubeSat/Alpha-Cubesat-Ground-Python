import { createContext, useContext, useEffect, useState } from "react";
import { useApi } from "./ApiProvider";

const UserContext = createContext();

// User Context Provider
// Keeps track of currently logged-in user and contains authentication related functions
export default function UserProvider({ children }) {
  const [user, setUser] = useState();
  const api = useApi();

  // automatically fetch user details when ground station is first loaded
  useEffect(() => {
    userFromToken();
  }, [api]);

  // If a token exists, fetch basic user data from the API
  // If the request fails, the user is not logged in
  const userFromToken = () => {
    if (localStorage.getItem("token") !== null) {
      api
        .get("/user/")
        .then((response) => {
          setUser(response.data);
        })
        .catch((e) => {
          console.log(e);
          setUser(null);
        });
    } else {
      setUser(null);
    }
  };

  // Logs in a user with their username and password
  const login = async (username, password) => {
    await api
      .post(
        "/auth/token",
        {},
        {
          headers: {
            Authorization: "Basic " + btoa(username + ":" + password),
          },
        }
      )
      .then((res) => {
        localStorage.setItem("token", res.data["access_token"]);
        userFromToken();
      })
      .catch((e) => {
        console.log(e);
        setUser(null);
      });
  };

  // Logs out a user
  const logout = async () => {
    api.delete("/auth/token").then((res) => {
      localStorage.removeItem("token");
      setUser(null);
    });
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  return useContext(UserContext);
}
