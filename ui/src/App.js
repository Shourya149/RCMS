import {BrowserRouter as Router,Routes,Route} from 'react-router-dom';
import Register from './Pages/Register';
import LogIn from './Pages/LogIn';
import Form from './Pages/Form';

//Regiistering our application routes
function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
            <Route path="/register" element={<Register/>}/>
            <Route path="/" exact element={<LogIn/>}/>
            <Route path="/form" element={<Form/>}/>
        </Routes>
      </Router>
    </div>
  );
}

export default App;
