import React, { useState } from 'react'
import './LoginSignUp.css'
import { useNavigate } from 'react-router-dom'


const LoginSignup = () => {

    const [action, setAction] = useState("Login");
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const validateForm = () => {
        if (action === "Sign Up" && (!username || !password || !email)) {
            setError('Username, Email, and Password are required');
            return false;
        }
        if (action === "Login" && (!username || !password)) {
            setError('Username and Password are required');
            return false;
        }

        setError('');
        return true;
    };

    async function handleSubmit(event) {
        event.preventDefault();
        if (!validateForm()) return;
        setLoading(true)

        try {
            const url = action === "Login" ? 'http://localhost:8000/auth/login' : 'http://localhost:8000/auth/register'
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',

                },
                credentials: "include",
                body: JSON.stringify(
                    action === "Login"
                        ? { username: username, password: password }
                        : { username: username, password: password, email: email }

                ),
            });
            if (response.ok) {
                const data = await response.json();
                const access_token = data.access_token;
                localStorage.setItem("access_token", access_token); //less secure

                setLoading(false);

                if (access_token) {
                    navigate('/dashboard')

                }
                else {
                    console.error('something wrong')
                }
            } else {
                // Handle error response (401, 409, etc.)
                const errorData = await response.json();
                setError(errorData.detail || 'Login failed');
                setLoading(false);
            }
        } catch (err) {
            console.error(err)
            setLoading(false);
            setError(err.message || 'Something went wrong. Please try again.')

        }

    }


    return (
        <div className='container'>
            <div className="header">
                <div className='text'>{action}</div>
                <div className="underline"></div>
            </div>
            <form onSubmit={handleSubmit}>
                {error && <div className="error-message">{error}</div>}
                <div className="inputs">
                    {action === "Login" ? (
                        <>
                            <div className="input">
                                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                            </div>
                            <div className="input">
                                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="input">
                                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                            </div>
                            <div className="input">
                                <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                            </div>
                            <div className="input">
                                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                            </div>
                        </>
                    )}
                </div>

                <div className="submit-continer">
                    <button type="submit" className="submit" disabled={loading}>
                        {loading ? 'Loading...' : action}
                    </button>
                    {action === "Login" ? (
                        <div className="forgot-password">Lost Password?<span>Click Here!</span></div>
                    ) : null}
                    <div className="toggle-text">
                        {action === "Login" ? (
                            <>Don't have an account? <span onClick={() => setAction("Sign Up")}>Sign Up</span></>
                        ) : (
                            <>Already have an account? <span onClick={() => setAction("Login")}>Login</span></>
                        )}
                    </div>
                </div>
            </form>
        </div>
    )
}

export default LoginSignup