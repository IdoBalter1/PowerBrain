import React, { useState } from 'react'
import './LoginSignUp.css'


const LoginSignup = () => {

    const [action, setAction] = useState("Login")
    return (
        <div className='container'>
            <div className="header">
                <div className='text'>{action}</div>
                <div className="underline"></div>
            </div>
            <div className="inputs">
                {action === "Login" ? (
                    <>
                        <div className="input">
                            <input type="text" placeholder="Username" />
                        </div>
                        <div className="input">
                            <input type="password" placeholder="Password" />
                        </div>
                    </>
                ) : (
                    <>
                        <div className="input">
                            <input type="text" placeholder="Username" />
                        </div>
                        <div className="input">
                            <input type="email" placeholder="Email" />
                        </div>
                        <div className="input">
                            <input type="password" placeholder="Password" />
                        </div>
                    </>
                )}
            </div>
            {action === "Login" ? (
                <div className="forgot-password">Lost Password?<span>Click Here!</span></div>
            ) : null}
            <div className="submit-continer">
                <div className={action === "Login" ? "submit gray" : "submit"} onClick={() => { setAction("Sign Up") }}>Sign Up</div>
                <div className={action === "Sign Up" ? "submit gray" : "submit"} onClick={() => { setAction("Login") }}>Login</div>
            </div>
        </div>
    )
}

export default LoginSignup