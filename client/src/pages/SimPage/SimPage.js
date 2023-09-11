import "./SimPage.scss";
import PulseGraph from '../../components/PulseGraph/PulseGraph';
import { useState, useEffect } from "react";
import Form from 'react-bootstrap/Form';
import Slider from '@mui/material/Slider';
import SimGraph from "../../components/SimGraph/SimGraph";

function SimPage() {
    const [currentPulse, setCurrentPulse] = useState({
        'type': 'Choose Pulse',
        'graph_data': {
            'xdata': '[]',
            'ydata': '[]',
            'phase': '[]',
        },
        'graph_params': [],
        'sim_params': [],
        'sim_data': {
            'xdata': '[]',
            'mxy': '[]',
            'mz': '[]'
        }
    });
    
    // When page is loaded, get default data from backend
    useEffect(() => {
        fetch('/pulse').then(res => res.json()).then(data => {
            setCurrentPulse(({
            type: data.type,
            graph_data: {
                'xdata': data.graph_data.xdata,
                'ydata': data.graph_data.ydata,
                'phase': data.graph_data.phase,
            },
            graph_params: JSON.parse(data.graph_params),
            sim_params: JSON.parse(data.sim_params),
            sim_data: {
                'xdata': data.sim_data.xdata,
                'mxy': data.sim_data.mxy,
                'mz': data.sim_data.mz
            }
            }));
        });
        }, []);
    
        // Sends new pulse type to api to recalculate values
        let handleTypeChange = (event) => {
        fetch('/pulsechange', {
            method:"POST",
            cache:"no-cache",
            headers:{
                "Content_Type":"application/json",
                "Accept":"application/json",
            },
            body:JSON.stringify({
                type: event.target.value
            })
        })
        .then(res => res.json())
        .then(data => {
            setCurrentPulse(({
            type: data.type,
            graph_data: {
                'xdata': data.graph_data.xdata,
                'ydata': data.graph_data.ydata,
                'phase': data.graph_data.phase,
            },
            graph_params: JSON.parse(data.graph_params),
            sim_params: JSON.parse(data.sim_params),
            sim_data: {
                'xdata': data.sim_data.xdata,
                'mxy': data.sim_data.mxy,
                'mz': data.sim_data.mz
            }
            }));
        })
    }

    
    // Updates graph values based on new parameters
    let handleGraphParamChange = (event) => {
        const newParams = (currentPulse.graph_params).map(param => {
            if (param.name == event.target.name) {
                return {
                    ...param,
                    val: event.target.value
                }
            } else {
                return param;
            }
        })
        // Fetch new data
        fetch('/pulsegraphparamchange', {
            method:"POST",
            cache:"no-cache",
            headers:{
                "Content_Type":"application/json",
                "Accept":"application/json",
            },
            body:JSON.stringify({
                type: currentPulse.type,
                graph_params: JSON.stringify(newParams),
                sim_params: JSON.stringify(currentPulse.sim_params)
            })
        })
        .then(res => res.json())
        .then(data => {
            setCurrentPulse(({
            ...currentPulse,
            graph_params: JSON.parse(data.graph_params),
            graph_data: {
                'xdata': data.graph_data.xdata,
                'ydata': data.graph_data.ydata,
                'phase': data.graph_data.phase,
            },
            sim_data: {
                'xdata': data.sim_data.xdata,
                'mxy': data.sim_data.mxy,
                'mz': data.sim_data.mz,
            }
            }));
        })
    }; 

    // Updates graph values based on new parameters
    let handleSimParamChange = (event) => {
        const newParams = (currentPulse.sim_params).map(param => {
            if (param.name == event.target.name) {
                return {
                    ...param,
                    val: event.target.value
                }
            } else {
                return param;
            }
        })
        // Fetch new data
        fetch('/pulsesimparamchange', {
            method:"POST",
            cache:"no-cache",
            headers:{
                "Content_Type":"application/json",
                "Accept":"application/json",
            },
            body:JSON.stringify({
                type: currentPulse.type,
                graph_data: currentPulse.graph_data,
                graph_params: JSON.stringify(currentPulse.graph_params),
                sim_params: JSON.stringify(newParams)
            })
        })
        .then(res => res.json())
        .then(data => {
            setCurrentPulse(({
            ...currentPulse,
            sim_params: data.sim_params,
            sim_data: {
                'xdata': data.sim_data.xdata,
                'mxy': data.sim_data.mxy,
                'mz': data.sim_data.mz,
            }
            }));
        })
    }; 

    return (
        <div className="sim">
            <div className="options">
                <div className="choices">
                    <div className="pulse-choice">
                        <Form.Select onChange={handleTypeChange}>
                            <option value="none">Choose Pulse</option>
                            <option value="sinc">Sinc</option>
                            <option value="gauss">Gaussian</option>
                            <option value="square">Square</option>
                            <option value="HSn">HSn</option>
                        </Form.Select>
                    </div>
                    <div>{currentPulse.graph_params.map((param, index) => {
                        return (
                            <div key={`${param}`}>
                                <div className="param-name">{param.name}</div>
                                <div>
                                    <Slider sx={{
                                        '& .MuiSlider-thumb': {
                                            color: "#61919F"
                                        },
                                        '& .MuiSlider-track': {
                                            color: "#61919F"
                                        },
                                        '& .MuiSlider-rail': {
                                            color: "#61919F"
                                        },
                                        '& .MuiSlider-active': {
                                            color: "#61919F"
                                        }
                                    }}
                                        defaultValue={param.val}
                                        step={param.step}
                                        min={param.min}
                                        max={param.max}
                                        name={param.name}
                                        valueLabelDisplay="auto"
                                        onChange={handleGraphParamChange}
                                    />
                                </div>
                            </div>
                        )
                    })}</div>
                </div>
                <div className="graph">
                    <PulseGraph data={currentPulse.graph_data} />
                </div>
            </div>
            <div className="options">
                <div className="choices">
                <div>{currentPulse.sim_params.map((param, index) => {
                        return (
                            <div key={`${param}`}>
                                <div className="param-name">{param.name}</div>
                                <div>
                                    <Slider sx={{
                                        '& .MuiSlider-thumb': {
                                            color: "#61919F"
                                        },
                                        '& .MuiSlider-track': {
                                            color: "#61919F"
                                        },
                                        '& .MuiSlider-rail': {
                                            color: "#61919F"
                                        },
                                        '& .MuiSlider-active': {
                                            color: "#61919F"
                                        }
                                    }}
                                        defaultValue={param.val}
                                        step={param.step}
                                        min={param.min}
                                        max={param.max}
                                        name={param.name}
                                        valueLabelDisplay="auto"
                                        onChange={handleSimParamChange}
                                    />
                                </div>
                            </div>
                        )
                    })}
                </div>
                </div>
                <div className="graph">
                    <SimGraph data={currentPulse.sim_data} />
                </div>
            </div>
        </div>
    );
}

export default SimPage;
