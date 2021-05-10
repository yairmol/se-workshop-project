import {useState} from "react";
import {
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  FormGroup
} from "@material-ui/core";
import Button from "@material-ui/core/Button";

export default function RemoveAppointmentPopup({worker, close_window_func, unappoint_manager_func, unappoint_owner_func}) {
  const [open, setOpen] = useState(true)

  const handleClose = () => {
    setOpen(false)
    close_window_func()
  }

  const done = () => {
    if (worker.title === "manager") {
      unappoint_manager_func(worker.username)
    } else {
      unappoint_owner_func(worker.username)
    }
    handleClose()
  }

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Are you sure you want to remove appointment of {worker.title} {worker.name}?
        </DialogTitle>
        <DialogActions>
          <Button onClick={done} color="primary">
            yes
          </Button>
          <Button onClick={handleClose} color="primary" autoFocus>
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
