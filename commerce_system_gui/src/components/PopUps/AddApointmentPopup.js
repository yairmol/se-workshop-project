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

export default function AddAppointmentPopup({shop_id, close_window_func, appoint_manager_func, appoint_owner_func}) {
  const [open, setOpen] = useState(true)
  const [show_perms, set_show_perms] = useState(true)

  const [username, setName] = useState("")
  const [state, setState] = useState({
    delete_product: false,
    edit_product: false,
    add_product: false,
    manage_discounts: false,
    watch_transactions: false,
    watch_staff: false
  });

  const handleSelectChange = (event) => {
    set_show_perms(event.target.value);
  };

  const handleClose = () => {
    setOpen(false)
    close_window_func()
  }

  const { delete_product, edit_product, add_product, manage_discounts, watch_transactions, watch_staff } = state;

  const done = () => {
    if (show_perms) {
      // ADD MANAGER
      const perms = [
        [delete_product, "delete_product"], [edit_product, "edit_product"],
        [add_product, "add_product"], [manage_discounts, "manage_discounts"],
        [watch_transactions, "watch_transactions"], [watch_staff, "watch_staff"]
      ]
      let perms_lst = []
      for (let i =0; i<perms.length; i++) {
        if (perms[i][0]) {
          perms_lst.push(perms[i][1])
        }
      }
      appoint_manager_func(username, perms_lst)
    } else {
      // ADD OWNER
      appoint_owner_func(username)
    }
    handleClose()
  }

  const handleChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

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
              control={<Checkbox checked={delete_product} onChange={handleChange} name="delete_product" />}
              label="Delete product"
            />
            <FormControlLabel
              control={<Checkbox checked={edit_product} onChange={handleChange} name="edit_product" />}
              label="Edit product"
            />
            <FormControlLabel
              control={<Checkbox checked={add_product} onChange={handleChange} name="add_product" />}
              label="Add product"
            />
            <FormControlLabel
              control={<Checkbox checked={manage_discounts} onChange={handleChange} name="manage_discounts" />}
              label="Edit discounts"
            />
            <FormControlLabel
              control={<Checkbox checked={watch_transactions} onChange={handleChange} name="watch_transactions" />}
              label="View transactions"
            />
            <FormControlLabel
              control={<Checkbox checked={watch_staff} onChange={handleChange} name="watch_staff" />}
              label="View Shop Staff"
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
