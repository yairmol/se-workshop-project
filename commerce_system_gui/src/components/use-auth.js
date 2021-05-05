import React, {useState, useEffect, useContext, createContext} from "react";
import {enter, exit, login, logout, register} from "../api";

const authContext = createContext();

// Provider component that wraps your app and makes auth object
// available to any child component that calls useAuth().
export function ProvideAuth({children}) {
  const auth = useProvideAuth();
  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

// Hook for child components to get the auth object
// and re-render when it changes.
export const useAuth = () => {
  return useContext(authContext);
};

// Provider hook that creates auth object and handles state
function useProvideAuth() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(localStorage.getItem("user"));

  const signin = (username, password) => {
    return login(token, username, password)
        .then((response) => {
          if (response) {
            setUser(username);
            localStorage.setItem("user", username)
            return username;
          }
        });
  };
  const signup = (userData) => {
    return register(token, userData)
        .then((response) => {
          return response;
        });
  };
  const signout = () =>
      logout(token).then((res) => {
        if (res) {
          localStorage.removeItem("user")
          setUser(null);
          return true
        }
        return false
      });

  useEffect(async () => {
    localStorage.clear();
    alert(`user token ${token}`);

    if (!token) {

      await enter().then((new_token) => {
        localStorage.setItem("token", new_token)
        setToken(new_token);
        register(new_token, {username: 'yairmol', password: 'mypassword'});
      })
    }

    if (user) {
      setUser(user);
    }

    // return () => {
    //   alert(`exiting ${localStorage.getItem("token")}`)
    //   exit(localStorage.getItem("token"));
    //   localStorage.clear();
    // }
  }, []);

  // Return the user object and auth methods
  return {
    token,
    user,
    signin,
    signup,
    signout,
  };
}