import React, {useState, useEffect, useContext, createContext, useCallback} from "react";
import {enter, isValidToken, login, logout, register} from "../api";
import startNotifications from "../notifs";
import {useHistory} from "react-router-dom";

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
  const [notifications, setNotifications] = useState(null);
  const [notificationsList, setNotificationsList] = useState([]);
  const history = useHistory();

  const onNotificationReceived = useCallback((msg) => {
    // alert("got message");
    console.log(`notifications: ${JSON.stringify(notificationsList)}`)
    console.log(`got message ${msg}`);
    setNotificationsList([msg, ...notificationsList]);
  }, [notificationsList])

  const getToken = useCallback(() => {
    // alert("in get token");

    const refresh = () => {
      // alert("in refresh")
      localStorage.clear();
      setUser(null);
      setUserId(null);
      return enter().then((data) => {
        if (data.id) {
          const _notifications = startNotifications();
          _notifications.enlist(data.id);
          _notifications.registerNotifHandler(onNotificationReceived);
          console.log("registered notifications handler");
          setNotifications(_notifications)
        }
        localStorage.setItem("token", data.result)
        localStorage.setItem("userId", data.id)
        setToken(data.result)
        setUserId(data.id)
        return data.result;
      })
    }

    if (token) {
      return isValidToken(token).then((res) => {
        if (res) {
          return token
        } else {
          // alert("res is false")
          return refresh().then((token) => {
            history && history.replace({pathname: "/", header: "Main Page"})
            return token;
          })
        }
      })
    } else {
      // alert("token is null")
      return refresh().then(_ => history && history.replace({pathname: "/", header: "Main Page"}))
    }
  }, [history, token, onNotificationReceived])
    // if (!token || !(await isValidToken(token))) {
    //   localStorage.clear();
    //   await enter().then((data) => {
    //     localStorage.setItem("token", data.result)
    //     setToken(data.result);
    //     localStorage.setItem("userId", data.id)
    //     setUserId(data.id);
    //     alert(`here ${data.result}`)
    //     return data.result;
    //   })
    // }
    // return token;

  const signin = (username, password) => {
    return getToken().then((_token) =>
      login(_token, username, password)
        .then((response) => {
          if (response) {
            setUser(username)
            localStorage.setItem("user", username)
            return username;
          }
        })
    )
  };

  useEffect(() => {
    console.log("in use effect");
    isValidToken(token).then((res) => {
      if (res) {
        if ((!notifications || !notifications.isConnected()) && userId) {
          const _notifications = startNotifications();
          _notifications.enlist(userId);
          _notifications.registerNotifHandler(onNotificationReceived);
          console.log("reconnected notifications");
          setNotifications(_notifications);
        } else {
          console.log("updating notifications handler");
          notifications.registerNotifHandler(onNotificationReceived);
        }
      }
    })
  }, [token, user, userId, notifications, onNotificationReceived])

  const signup = (userData) => {
    return getToken().then((_token) =>
      register(_token, userData)
        .then((response) => {
          return response;
        })
    )
  };

  const signout = () =>
    logout(token).then((res) => {
      localStorage.removeItem("user")
      setUser(null);
      return res
    });

  // Return the user object and auth methods
  return {
    getToken,
    user,
    userId,
    signin,
    signup,
    signout,
    notificationsList,
    setNotificationsList,
  };
}