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
    delete_p: permissions.delete,
    edit: permissions.edit,
    add: permissions.add,
    discount: permissions.discount,
    transaction: permissions["transaction"],
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
    const perms =
        [[delete_p, "delete"], [edit, "edit"], [add, "add"], [discount, "discount"], [transaction, "transaction"]]
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
          Edit permissions for manager {worker.name}
        </DialogTitle>
        <DialogContent>
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
