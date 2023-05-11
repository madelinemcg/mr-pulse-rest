import "./HomePage.scss";
import PulseGraph from '../../components/PulseGraph/PulseGraph';
import { useState, useEffect } from "react";
import Form from 'react-bootstrap/Form';

function HomePage() {
  const [currentPulse, setCurrentPulse] = useState({
    'type': 'Choose Pulse',
    'graph_data': '[]',
  });

  // When page is loaded, get data from backend
  useEffect(() => {
    fetch('/pulse').then(res => res.json()).then(data => {
      setCurrentPulse(({
        type: data.type,
        graph_data: data.graph_data
      }));
    });
  }, []);

  // Sends data to backend and updates state
  let handleTypeChange = (event) => {
    fetch('/pulsechange', {
      method:"POST",
        cache:"no-cache",
        headers:{
            "Content_Type":"application/json",
            "Accept":"application/json",
        },
        body:JSON.stringify({
          graph_data: currentPulse.graph_data,
          type: event.target.value
        })
    })
    .then(res => res.json())
    .then(data => {
      setCurrentPulse(({
        type: data.type,
        graph_data: data.graph_data
      }));
    });
  }

    return (
      <div className="home">
        <p>Home Page</p>
        <p>Current pulse type is {currentPulse.type}</p>
        <Form.Select onChange={handleTypeChange}>
          <option value="none">Choose Pulse</option>
          <option value="sinc">Sinc</option>
          <option value="gauss">Guassian</option>
        </Form.Select>
        <p>Current pulse data is {currentPulse.graph_data}</p>
        <PulseGraph />
      </div>
    );
};

export default HomePage;
