import {useState} from 'react';
import axios from 'axios';
import {Navigate} from 'react-router-dom';
import './RegisterStyle.css';



function Register(){

    const [credentials,setCredentials] =useState({});
    const[message,setMessage] =useState("")

    //To store data entered into the input field
    const handleChange = (event) =>{
        const name = event.target.name;
        const value= event.target.value;

        setCredentials (values => ({...values , [name] : value}))
    }

    
    //Sending data (user name , uuser email and password) to backend to register
    const handleSubmit = async (event) =>{

        event.preventDefault();
        
        try {
            const response =await axios.post( 'http://127.0.0.1:8000/rcms/signup',credentials);
        
            setMessage(response.data.Name);

        }catch(error){
            
        }
    }


    //User Layout
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
                    <h2 style={{"color" : "whitesmoke" , "margin-left" : "60px" }}><u>Register</u></h2>
                </center>
            </div>

            <div className="registration-form">
                <form onSubmit={handleSubmit}>
                    <label htmlFor="name">Name:</label>
                    <input type="text" id="name" name="name"  placeholder="Username"  onChange={handleChange} required/>
                    <label htmlFor="email">Email:</label>
                    <input type="email" id="email" name="email" placeholder="Email"  onChange={handleChange} required/>
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" placeholder="Password" onChange={handleChange} required/>
                    <button type="submit" className="register-button">Register</button>
                </form>
            </div>

            <div>
                {message && <Navigate to="/" replace={true} />}
            </div>
        </div>
        
    );
}

export default Register;