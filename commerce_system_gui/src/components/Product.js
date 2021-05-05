import {useEffect, useState} from "react";
import {delete_product, edit_product, get_permissions, get_product_info} from "../api";
import React from "react";
import {
  useParams, Link as RouteLink
} from "react-router-dom";
import {useAuth} from "./use-auth";
import Button from "@material-ui/core/Button";
import {makeStyles} from '@material-ui/core/styles';
import {TextField} from "@material-ui/core";


const useStyles = makeStyles({
  root: {
    maxWidth: 2000,
  },
  media: {
    height: 500,
  },
});

export const Product = ({shop_name}) => {
  const classes = useStyles();
  const auth = useAuth()

  const [product, setProduct] = useState(false);
  let {shop_id, product_id} = useParams();

  const [permissions, setPermissions] = useState(false);
  const [name, setName] = useState(product.product_name);
  const [price, setPrice] = useState(product.price);
  const [description, setDescription] = useState(product.description);
  const [categories, setCategories] = useState(product.categories);

  useEffect(() => {

    if (!product) {
      get_product_info(auth.token, 1, 1).then((res) => {
        setProduct(res)
      });
    }
    if (!permissions) {
      get_permissions(auth.token, 1).then((res) => {
        setPermissions(res)
      });
    }
  })


  const onSubmitEdit = (e) => {
    e.preventDefault()
    // WHAT TO DO WITH then.. ?
    edit_product(auth.token, shop_id, product_id, name, price, description, categories)
  }
  const onSubmitDelete = (e) => {
    e.preventDefault()
    delete_product(auth.token,shop_id, product_id)
  }


  return (
      <form>
            <table>
              <tr> <h1> {shop_name} </h1></tr>
              <tr><td>{product.product_name}</td> <td><TextField id="standard-basic"  label="New Name" onChange={(e) => setName(e.target.value)}/></td></tr>
              <tr><td>Price{product.price}</td> <td><TextField id="standard-basic" label="New Price" onChange={(e) => setPrice(e.target.value)}/></td></tr>
              <tr><td>Description:{product.description}</td><td><TextField id="standard-basic" label="New Description" onChange={(e) => setDescription(e.target.value)}/></td></tr>
              <tr><td>Categories:{product.categories}</td><td><TextField id="standard-basic" label="New Categories" onChange={(e) => setCategories(e.target.value)}/></td></tr>
              <tr>  {/* For Regular User */}
                <Button variant="contained" color="primary"> Buy Now </Button></tr>
              <tr>  {/* For Owner/Manager */}
                 {permissions.edit ? <Button onClick={onSubmitEdit} variant="contained" color="primary" >
                  Edit Product </Button> : <> </>}
                  {permissions.delete ? <Button onClick={onSubmitDelete} variant="contained" color="primary" href="/">
                  Delete Product </Button> : <> </>}
                </tr>
            </table>
      </form> );

}
      // <Card className={classes.root}>
      //   <CardActionArea>
      //     {/*<CardMedia*/}
      //     {/*  className={classes.media}*/
      //     }
      //     {/*  image="/static/images/cards/contemplative-reptile.jpg"*/
      //     }
      //     {/*  title="Contemplative Reptile"*/
      //     }
      //     {/*/>*/
      //     }
      //   </CardActionArea>
      //   <CardContent>
      //     <Typography gutterBottom variant="h2" component="h1">
      //       {
      //         product.product_name
      //       }
      //       -{shop_name}
      //     </Typography>
      //     <Typography variant="body1" color="textSecondary" component="p">
      //       <table>
      //         <tr>
      //           <td>Price:
      //             {
      //               product.price
      //             }
      //           </td>
      //           <td><TextField id="standard-basic" label="New Price"/></td>
      //         </tr>
      //         <tr>
      //           <td>Description:
      //             {
      //               product.description
      //             }
      //           </td>
      //           <td><TextField id="standard-basic" label="New Description"/></td>
      //         </tr>
      //         <tr>
      //           <td>Categories:
      //             {
      //               product.categories
      //             }
      //           </td>
      //           <td><TextField id="standard-basic" label="New Categories"/></td>
      //         </tr>
      //       </table>
      //     </Typography>
      //   </CardContent>
      //
      //   {/* For Regular User */
      //   }
      //   <CardActions>
      //     <Button variant="contained" color="primary" href="purchase_product/${product_id}">
      //       Buy Now
      //     </Button>
      //   </CardActions>
      //   {/* For Owner/Manager */}
      //   <CardActions>
      //     {permissions.edit ? <Button onClick={onSubmitEdit} variant="contained" color="primary" href="purchase_product/${product_id}">
      //       Edit Product
      //     </Button> : <> </>}
      //     {permissions.delete ? <Button onClick={onSubmitDelete} variant="contained" color="primary" href="purchase_product/${product_id}">
      //       Delete Product
      //     </Button> : <> </>}
      //   </CardActions>
      // </Card>
