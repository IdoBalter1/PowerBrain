import React, { useState, useEffect } from 'react'
import api from './services/api.js'
import LoginSignup from './components/loginSignUp/LoginSignUp.jsx'

const App = () => {
    return (
        <div>
            <LoginSignup/>
        </div>
    )
}

export default App


