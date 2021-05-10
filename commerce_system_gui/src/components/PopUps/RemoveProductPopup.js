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

export default function RemoveProductPopup({product, close_window_func, remove_product_func}) {
  const [open, setOpen] = useState(true)

  const handleClose = () => {
    setOpen(false)
    close_window_func()
  }

  const done = () => {
    /*
    CALL FOR REMOVE PRODUCT
     */
    remove_product_func(product.product_id)
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
          Are you sure you want to remove {product.product_name}? (id = {product.product_id})
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
