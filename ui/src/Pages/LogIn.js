import {Link,useNavigate} from 'react-router-dom';
import {useEffect, useState} from 'react';
import {decodeToken} from "react-jwt";
import axios from 'axios';


function LogIn(){

    const[credentials,setCredentials] = useState({});
    
    const redirect =useNavigate();

    
    //Function block to send request to check for expird tokens 
    const validatedata=async() => {

        try{
            const response= await axios.post('http://127.0.0.1:8000/rcms/expired',
                    {"Token" : localStorage.getItem('Token')})

            //If token not expired, redirect to form page 
            if(response.data.expired === 'False')
              redirect('/form');
            else
                localStorage.clear();
        }catch(err){

        }} 

    
    //Checking for token eexpiry    
    useEffect(() => {
        if(localStorage.getItem('Token') ){
            validatedata();
        }
    })


    //Storing values enterd into the input field
    const handleChange = (event) =>{
        const name = event.target.name;
        const value= event.target.value;

        setCredentials(values => ({...values , [name] : value}));
    }

    //Submitting data to backend (user email and password) in order to login
    const handleSubmit = async (event) =>{

        event.preventDefault();
        
        try {
            const response =await axios.post( 'http://127.0.0.1:8000/rcms/signin',credentials );
        
            //Retrieving token from server 
            const token=response.data.Token;
            console.log(token);

            const decoded_data=decodeToken(token);
            
            //Storing token in the localstorage(cookies to be used in future)
            localStorage.setItem('Token',token);
            localStorage.setItem('Name',decoded_data.name);

            redirect('/form');
            
        }catch(error){
            
        }

        
        
    }


    //Layout of the page
    return(
        <div>
            <div className="container">
                <header>
                    <div className="logo">
                        <img src="2.png" alt="Logo"/>
                        <h1>Road Construction Management System</h1>
                    </div>
                </header>
            </div>

            <div>
                <center>
                    <h2 style={{"color" : "whitesmoke" , "margin-left" : "60px" }}><u>Log In</u></h2>
                </center>
            </div>

            <div className="registration-form">
                <form onSubmit={handleSubmit}>
                    <label htmlFor="email">Email:</label>
                    <input type="email" id="email" name="email" placeholder="Email" required onChange={handleChange}/>
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" placeholder="Password" required onChange={handleChange}/>
                    <button type="submit" className="register-button">Log In</button>
                    <br/>
                    <br/>
                    <p> 
                        <Link to="/register">Register If New User </Link>
                    </p>
                </form>
            </div>
        
        </div>
    );
}

export default LogIn;