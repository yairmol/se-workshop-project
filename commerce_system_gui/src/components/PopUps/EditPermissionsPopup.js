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

export default function EditWorkerPermissions({worker, close_window_func, edit_perms_func, promote_manager}) {
  const permissions = worker.permissions
  const [open, setOpen] = useState(true)

  const [state, setState] = useState({
    delete_product: permissions.delete_product,
    edit_product: permissions.edit_product,
    add_product: permissions.add_product,
    manage_discounts: permissions.manage_discounts,
    watch_transactions: permissions.watch_transactions,
    watch_staff: permissions.watch_staff,
  });

  const handleClose = () => {
    setOpen(false)
    close_window_func()
  }

  const done = () => {
    /*
    CALL FOR SET PERMISSIONS
     */
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
    edit_perms_func(worker.username, perms_lst)
    handleClose()
  }

  const promote_manager_done = () => {
    promote_manager(worker.username)
    handleClose()
  }

  const handleChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  const { delete_product, edit_product, add_product, manage_discounts, watch_transactions, watch_staff } = state;

  return (
    <div>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          Edit permissions for manager {worker.name}
        </DialogTitle>
        <DialogContent>
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
        </DialogContent>
        <DialogActions>
          <Button onClick={promote_manager_done} color="secondary">
            Promote To Owner
          </Button>
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
