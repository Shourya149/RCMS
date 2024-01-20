import axios from "axios";
import {useState , useEffect ,useRef} from "react";
import { useNavigate} from "react-router-dom";
import "./FormStyle.css";



function Form(){

    const redirect = useNavigate();
    const ref=useRef(null);
    
    //To make our route protected
    useEffect(() => {
        if(!localStorage.getItem('Token') ){
            redirect('/');
        }
    })

    
    const[address,setAddress]=useState({});
    const[contractor,setContrator]=useState("");
    const[bidvalue,setBidvalue]=useState(0.0)
    
    
    //Funnction to logout
    const handleQuit = () => {
        localStorage.clear();
        redirect('/');
    }

    //Storing values enterd into the input field     
    const handleChange = (event) => {
        const name = event.target.name;
        const value= event.target.value;

        setAddress(values => ({...values , [name] : value}));
    }
    
    //Submiting data to backend
    const handleSubmit= async (event) => {

        event.preventDefault();

        try{
            const response= await axios.post('http://127.0.0.1:8000/rcms/bid', address);
            //Rettrieving value of winning bid from response
            const value_of_bid=response.data.bid;
            //Retrieving name of contractor from response
            const name_of_contractor=response.data.name;
            setBidvalue(value_of_bid);
            setContrator(name_of_contractor);
            console.log(response.data);
        }catch(error){

        }
    }

    //Resetting the result and input field
    const clearAll= () => {
        ref.current.value = '';
        setBidvalue(0.0);
        setContrator("");
    }

    //Layout of the page
    return (
        <div>
            <div className="container">
                <header>
                    <div className="logo">
                        <img src="2.png" alt="Logo"/>
                        <h1>Road Construction Management System</h1>
                    </div>

                    <button className="logout-button" onClick={handleQuit}>
                        Log Out
                    </button>
                </header>
            </div>

            <div>
                <center>
                    <h2 style={{"color" : "whitesmoke" , "marginLeft" : "60px" }}><u>Welcome {localStorage.getItem("Name")} !!!</u></h2>
                </center>
            </div>

            <div className="registration-form">
                <form onSubmit={handleSubmit}>
                    <label htmlFor="address">Name of Road:</label>
                    <input type="text" id="address" ref={ref} name="road" placeholder="Address" required onChange={handleChange}/>
                    <div className="flex-container">
                        <br/>
                        <button className="btn btn-primary" type="submit" style={{"margin" : "0px 24px 0px 16px"}}>Send</button>
                    </div>
                </form>
                <br/>
                <button className="clear-button" onClick={clearAll}>Clear All</button>
            </div>

            <div>
                { contractor &&
                    <div className="d-flex justify-content-center align-items-center"> 
                        <div className="bg-success p-3 rounded w-25">
                            <div className="mb-3">    
                                <center>
                                    <p style={{"color" : "whitesmoke"}}>
                                        <h5><b><u>RESULTS</u></b></h5>
                                        Scheduled Contractor : {contractor}
                                        <br/>
                                        Bidding value :  Rs. {bidvalue}
                                        <br/>
                                    </p>
                                </center>
                            </div>    
                        </div>
                    </div>
                }
            </div>
        
        </div>
    )
}

export default Form;