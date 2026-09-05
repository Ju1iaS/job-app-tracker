import { useState, useEffect } from 'react';
import Login from './Login';
import { getApplications, getFunnel } from './api';


function App() {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [applications, setApplications] = useState([]);
    const [funnel, setFunnel] = useState(null);

    function handleLoginSuccess(newToken) {
        localStorage.setItem('token', newToken);
        setToken(newToken);
    }

    function handleLogout() {
        localStorage.removeItem('token');
        setToken(null);
    }

    async function loadData() {
        const apps = await getApplications(token);
        setApplications(apps);
        const funnelData = await getFunnel(token);
        setFunnel(funnelData);
    }

    useEffect(() => {
        if (token) {
          loadData();
        }
    }, [token]);

    if (!token) {
        return <Login onLoginSuccess={handleLoginSuccess} />;
    }

    return (
        <div>
            <h1>Job Application Tracker</h1>
            <button onClick={handleLogout}>Log out</button>
            <p>Applications loaded: {applications.length}</p>
            <p>Funnel data: {funnel ? JSON.stringify(funnel) : 'loading...'}</p>
        </div>
    );
}

export default App;