import React, {useState, useEffect, useContext, createContext} from "react";
import {enter, exit, isValidToken, login, logout, register} from "../api";
import notifs from "../notifs";

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
  const [userId, setUserId] = useState(localStorage.getItem("userId"));
  const getToken = async () => {
    if (!token || !(await isValidToken(token))) {
      localStorage.clear();
      await enter().then((data) => {
        localStorage.setItem("token", data.result)
        setToken(data.result);
        localStorage.setItem("userId", data.id)
        setUserId(data.id);
      })
    }
    return token;
  }

  const signin = async (username, password) => {
    return login(await getToken(), username, password)
        .then((response) => {
          if (response) {
            setUser(username);
            localStorage.setItem("user", username)
            return username;
          }
        });
  };

  const signup = async (userData) => {
    return register(await getToken(), userData)
        .then((response) => {
          return response;
        });
  };

  const signout = () =>
      logout(token).then((res) => {
        localStorage.removeItem("user")
        setUser(null);
        return res
      });

  useEffect(async () => {
    // localStorage.clear();
    await getToken();

    if (user) {
      setUser(user);
    }

    // return () => {
    //   alert(`exiting ${localStorage.getItem("token")}`)
    //   exit(localStorage.getItem("token"));
    //   localStorage.clear();
    // }
  }, []);

  const notif = notifs(); //
  notif.enlist(userId);// Change to user id

  const registerNotifHandler = (handler) =>{
    notif.registerNotifHandler(handler);
  }
  const registerNotifErrorHandler = (handler) =>{
     notif.registerNotifErrorHandler(handler);
  }
  const registerBroadcastHandler = (handler) =>{
     notif.registerBroadcastHandler(handler);
  }


  // Return the user object and auth methods
  return {
    getToken,
    user,
    userId,
    signin,
    signup,
    signout,
    registerNotifHandler,
    registerNotifErrorHandler,
     registerBroadcastHandler,
  };
}