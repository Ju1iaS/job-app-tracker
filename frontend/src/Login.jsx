import { useState } from 'react';
import { login, signup } from './api';

function Login({ onLoginSuccess }) {
    const [isSignup, setIsSignup] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    async function handleSubmit() {
        setError('');
        try {
        if (isSignup) {
            await signup(email, password);
        }
        const data = await login(email, password);
        onLoginSuccess(data.access_token);
        } catch (err) {
        setError(err.message);
        }
    }

    return (
        <div className="auth-screen">
        <h1>{isSignup ? 'Sign up' : 'Log in'}</h1>
        <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
        />
        <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleSubmit}>{isSignup ? 'Sign up' : 'Log in'}</button>
        {error && <p className="error">{error}</p>}
        <p>
            {isSignup ? 'Already have an account?' : "Don't have an account?"}{' '}
            <a href="#" onClick={() => setIsSignup(!isSignup)}>
            {isSignup ? 'Log in' : 'Sign up'}
            </a>
        </p>
        </div>
    );
}

export default Login;