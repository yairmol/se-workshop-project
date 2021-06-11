import {Fab} from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import React, {useCallback, useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import {
  appoint_shop_manager,
  appoint_shop_owner,
  edit_manager_permissions,
  get_shop_staff_info,
  promote_shop_owner,
  unappoint_manager,
  unappoint_shop_owner
} from "../api";
import Worker from "./Worker";
import AddIcon from "@material-ui/icons/Add";
import EditWorkerPermissions from "./PopUps/EditPermissionsPopup";
import RemoveAppointmentPopup from "./PopUps/RemoveAppointmentPopup";
import AddAppointmentPopup from "./PopUps/AddApointmentPopup";

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(20),
    flexBasis: '33.33%',
    flexShrink: 0,
    fontWeight: 530,
    padding: theme.spacing(1)
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
  info: {
    fontSize: theme.typography.pxToRem(15),

  },
  accordion: {
    flexGrow: 1
  },
  paper: {
    padding: theme.spacing(3),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
    textAlign: 'center'
  }
}));

export function ShopWorkers({shop_id, auth}) {
  const classes = useStyles();
  const [workers, set_workers] = useState([])
  const [load_workers_bool, set_load_workers] = useState(true)

  const load_workers_func = useCallback(() =>
    auth.getToken().then((token) =>
      get_shop_staff_info(token, shop_id).then((staff_info) => {
        set_workers(staff_info)
      })
    )
  , [auth, shop_id])

  useEffect(() => {
    if (load_workers_bool) {
      load_workers_func().then((_) => {
        set_load_workers(false)
      })
    }
  }, [load_workers_bool, load_workers_func])

  // for add appointment
  const [open_add_appointment, set_add_appointment] = useState(false)
  const open_add_app_window = () => {
    set_add_appointment(true)
  }

  //for removing appointment
  const [shop_worker_for_remove_app, set_worker_for_remove_app] = useState([])
  const [open_remove_app, set_remove_app] = useState(false)
  const open_remove_app_window = (worker) => {
    set_worker_for_remove_app(worker)
    set_remove_app(true)
  }

  // for editing manager permissions
  const [shop_worker_for_perms, set_worker_for_perms] = useState([])
  const [open_edit_permissions, set_edit_perms] = useState(false)
  const open_edit_perms_window = (worker) => {
    set_worker_for_perms(worker)
    set_edit_perms(true)
  }

  const promote_manager = (username) => {
    auth.getToken().then(token =>
      promote_shop_owner(token, shop_id, username).then((res) =>
        load_workers_func().then(_ => {
            if (res) {
              alert("Successfully Promoted Manager " + username)
            }
          }
        )))
  }

  const edit_perms_func = (username, permissions) => {
    auth.getToken().then(token =>
      edit_manager_permissions(token, shop_id, username, permissions).then(_ =>
        load_workers_func().then(_ =>
          alert("Successfully Edited Permissions Of Manager " + username)
        )))
  }

  const unappoint_owner_func = (username) => {
    auth.getToken().then(token =>
      unappoint_shop_owner(token, shop_id, username).then(_ =>
        load_workers_func().then(_ =>
          alert("Successfully Unappointed Owner " + username)
        )))
  }

  const unappoint_manager_func = (username) => {
    auth.getToken().then(token =>
      unappoint_manager(token, shop_id, username).then(_ =>
        load_workers_func().then(_ =>
          alert("Successfully Unappointed Manager " + username)
        )))
  }

  const appoint_owner_func = (username) => {
    auth.getToken().then(token =>
      appoint_shop_owner(token, shop_id, username).then(_ =>
        load_workers_func().then(_ =>
          alert("Successfully Appointed Owner " + username)
        )))
  }

  const appoint_manager_func = (username, permissions) => {
    auth.getToken().then(token =>
      appoint_shop_manager(token, shop_id, username, permissions).then(_ =>
        load_workers_func().then(_ =>
          alert("Successfully appointed Manager " + username)
        )))
  }

  return (
    <>
      <Grid item lg={6}>
        <Typography className={classes.heading}>Workers &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
          <Fab color="primary" onClick={open_add_app_window}
               aria-label="add" style={{height: '15px', width: '35px'}}>
            <AddIcon/>
          </Fab>
        </Typography>
        {(workers && workers.length > 0) ?
          workers.map((worker, index) => <div style={{width: '200%'}}>
            <Worker
              remove_appointment_func={open_remove_app_window}
              edit_permissions_func={open_edit_perms_window}
              key={index} user={auth.user} worker={worker}/></div>)
          : <Typography align="center">shop has no workers </Typography>
        }
      </Grid>
      {open_edit_permissions ?
        (<EditWorkerPermissions
          worker={shop_worker_for_perms}
          close_window_func={() => {
            set_edit_perms(false)
          }}
          edit_perms_func={edit_perms_func}
          promote_manager={promote_manager}
        />)
        : []}
      {open_remove_app ?
        (<RemoveAppointmentPopup
          worker={shop_worker_for_remove_app}
          close_window_func={() => {
            set_remove_app(false)
          }}
          unappoint_manager_func={unappoint_manager_func}
          unappoint_owner_func={unappoint_owner_func}
        />)
        : []}
      {open_add_appointment ?
        (<AddAppointmentPopup
          shop_id={shop_id}
          close_window_func={() => {
            set_add_appointment(false)
          }}
          appoint_owner_func={appoint_owner_func}
          appoint_manager_func={appoint_manager_func}
        />)
        : []}
    </>
  );
}