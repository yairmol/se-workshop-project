import React, {useState} from "react";
import {
  Checkbox,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle, FormControl,
  FormControlLabel,
  FormGroup, InputLabel, MenuItem, Radio, RadioGroup, Select, TextField
} from "@material-ui/core";
import Button from "@material-ui/core/Button";

export default function AddAppointmentPopup({shop_id, close_window_func}) {
  const [open, setOpen] = useState(true)
  const [show_perms, set_show_perms] = useState(true)

  const [username, setName] = useState("")
  const [state, setState] = useState({
    delete_p: false,
    edit: false,
    add: false,
    discount: false,
    transaction: false,
  });

  const handleSelectChange = (event) => {
    set_show_perms(event.target.value);
  };

  const handleClose = () => {
    setOpen(false)
    close_window_func()
  }

  const done = () => {
    if (show_perms) {
      // ADD MANAGER
    } else {
      // ADD OWNER
    }
    handleClose()
  }

  const handleChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  const { delete_p, edit, add, discount, transaction } = state;

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Add new appointment
        </DialogTitle>
        <DialogContent>
          <TextField autoFocus margin="dense" id="name" label="username" fullWidth
                       onChange={(e) => setName(e.target.value)} />
          <div style={{paddingTop: '15px', paddingBottom: '15px'}}>
          <form autoComplete="off">
        <FormControl >
          <InputLabel htmlFor="age-simple">Title</InputLabel>
          <Select
            value={show_perms}
            onChange={handleSelectChange}
            inputProps={{
              name: 'age',
              id: 'age-simple',
            }}
          >
            <MenuItem value={false}><div style={{padding: '5px'}}>Owner</div></MenuItem>
            <MenuItem value={true}><div style={{padding: '7px'}}>Manager</div></MenuItem>
          </Select>
        </FormControl>
          </form>
          </div>
          {show_perms ?
          <FormGroup>
            <FormControlLabel
              control={<Checkbox checked={delete_p} onChange={handleChange} name="delete_p" />}
              label="Delete product"
            />
            <FormControlLabel
              control={<Checkbox checked={edit} onChange={handleChange} name="edit" />}
              label="Edit product"
            />
            <FormControlLabel
              control={<Checkbox checked={add} onChange={handleChange} name="add" />}
              label="Add product"
            />
            <FormControlLabel
              control={<Checkbox checked={discount} onChange={handleChange} name="discount" />}
              label="Edit discounts"
            />
            <FormControlLabel
              control={<Checkbox checked={transaction} onChange={handleChange} name="transaction" />}
              label="View transactions"
            />
        </FormGroup>
              :
              []}
        </DialogContent>
        <DialogActions>
          <Button onClick={done} color="primary">
            Done
          </Button>
          <Button onClick={handleClose} color="primary" autoFocus>
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
