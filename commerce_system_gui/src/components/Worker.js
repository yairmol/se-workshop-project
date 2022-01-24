import {
    Accordion,
    AccordionDetails,
    AccordionSummary, Button,
    Tooltip
} from "@material-ui/core";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import {useState} from "react";
import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles((theme) => ({
    root: {
        width: '100%',
    },
    heading: {
        fontSize: theme.typography.pxToRem(20),
        flexBasis: '33.33%',
        flexShrink: 0,
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
    },
    button: {
        padding: theme.spacing(1),
        display: 'flex',
        overflow: 'auto',
        flexDirection: 'column',
        width: 200,
    },
    no_perms_button: {
        padding: theme.spacing(1),
        display: 'flex',
        overflow: 'auto',
        flexDirection: 'column',
    }
}));


export default function Worker({worker, user, edit_permissions_func, remove_appointment_func}) {
    const classes = useStyles();
    const [expanded, setExpanded] = useState(false);
    const onChange = () => {
        setExpanded(!expanded)
    }
    const is_manager = worker.title === "manager"
    const is_appointee = worker.appointer === user

    return (
        <Accordion expanded={expanded} onChange={onChange}>
            <AccordionSummary
                expandIcon={<ExpandMoreIcon/>}
            >
                <Grid container direction="column">
                    <Typography className={classes.heading}>{worker.username}</Typography>
                    <Typography className={classes.secondaryHeading}>title: {worker.title}</Typography>
                    <Typography className={classes.secondaryHeading}>appointer: {worker.appointer}</Typography>
                </Grid>
            </AccordionSummary>
            <AccordionDetails>
                {is_appointee ?
                <Grid container direction="column">
                    <Grid item align="center" style={{padding:'5px'}}>
                      <Button onClick={() => remove_appointment_func(worker)} size="small" className={classes.button} variant="contained" color="primary">
                          Remove appointment
                      </Button>
                    </Grid>
                    {is_manager ?
                    <Grid item size="small" align="center" style={{padding:'5px'}}>
                          <Button onClick={() => edit_permissions_func(worker)}
                                  className={classes.button}
                                  variant="contained" color="primary">
                            Edit permissions
                          </Button>
                    </Grid>
                    : [] }
                </Grid>
                    :
                    <Grid container direction="column">
                     <Grid item align="center" style={{padding:'5px'}}>
                         <Tooltip title="Worker not appointed by user" placement="top-center">
                             <div style={{width:'50%'}}>
                                  <Button size="small" disabled className={classes.button} variant="contained" color="primary">
                                      Remove appointment
                                  </Button>
                             </div>
                         </Tooltip>
                    </Grid>
                    {is_manager ?
                        <Grid item size="small" align="center" style={{padding:'5px'}}>
                            <Tooltip title="Worker not appointed by user">
                                <div style={{width:'50%'}}>
                                    <Button disabled className={classes.button} variant="contained" color="primary">
                                        Edit permissions
                                    </Button>
                                </div>
                            </Tooltip>
                        </Grid>: []}
                    </Grid>}
            </AccordionDetails>
        </Accordion>
    );
}