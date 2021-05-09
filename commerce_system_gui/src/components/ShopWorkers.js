import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Card,
    Divider, Fab,
    Link,
    List,
    ListItem,
    Paper
} from "@material-ui/core";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import React, {useEffect, useState} from "react";
import Grid from "@material-ui/core/Grid";
import {useAuth} from "./use-auth";
import {get_shop_staff_info} from "../api";
import Worker from "./Worker";
import AddIcon from "@material-ui/icons/Add";

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

export function ShopWorkers({shop_id, user, edit_permissions_func, remove_appointment_func, add_appointment_func}) {
    const classes = useStyles();
    const [expanded, setExpanded] = useState(false);
    const onChange = () => {
        setExpanded(!expanded)
    }
    const [load, set_load] = useState(true)
    const [workers, set_workers] = useState([])
    const auth = useAuth();
    useEffect(async () => {
        if (load) {
          await auth.getToken().then((token) => {
            get_shop_staff_info(token, shop_id).then((staff_info) => {
              set_workers(staff_info)
            })
          })
        }
        set_load(false)
      }, [])

    return (
        <>
        <Grid item lg={6} >
            <Typography className={classes.heading}>Workers &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                <Fab color="primary" onClick={() => add_appointment_func()}
                     aria-label="add" style={{ height:'15px', width:'35px' }} >
                  <AddIcon/>
                </Fab>
          </Typography>
          {(workers && workers.length > 0) ?
              workers.map((worker, index) => <div style={{width:'200%'}}>
                  <Worker
                      remove_appointment_func={remove_appointment_func}
                      edit_permissions_func={edit_permissions_func}
                      key={index} user={user} worker={worker}/></div>)
              : <Typography align="center">shop has no workers </Typography>
          }
        </Grid></>
    );
}