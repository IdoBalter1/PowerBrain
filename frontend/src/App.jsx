import React from 'react'
import { BrowserRouter } from 'react-router-dom'
import LoginSignup from './components/loginSignUp/LoginSignUp.jsx'

const App = () => {
    return (
        <BrowserRouter>
            <div>
                <LoginSignup />
            </div>
        </BrowserRouter>
    )
}

export default App


