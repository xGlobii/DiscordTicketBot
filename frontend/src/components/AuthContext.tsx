import React, { createContext, useContext, useEffect, useState } from "react";
import { type AuthDto } from "../models/AuthDto";

interface ContextType
{
    authData: AuthDto | null;
    setAuthData: React.Dispatch<React.SetStateAction<AuthDto | null>>;
    selectedGuild: string | null;
    setSelectedGuild: React.Dispatch<React.SetStateAction<string | null>>;
    isLogged: boolean;
    setIsLogged: React.Dispatch<React.SetStateAction<boolean>>;
    isLoading: boolean;
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const AuthContext = createContext<ContextType | null>(null);

export function AuthProvider({children}: {children: React.ReactNode})
{
    const [authData, setAuthData] = useState<AuthDto|null>(null);
    const [selectedGuild, setSelectedGuild] = useState<string|null>(null);
    const [isLogged, setIsLogged] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    useEffect(() =>
    {
        setIsLoading(true);

        fetch(`https://localhost:7219/api/v1/auth/me`, {method: "GET", headers: {"Content-Type": "application/json"}, credentials: "include"})
        .then(async (result) => 
        {
            if(result.ok)
            {
                const data = await result.json()
                setAuthData(data);
                setIsLogged(true);

            }
            if(result.status === 401)
            {
                setAuthData(null);
                setIsLogged(false);
            }
        })
        .finally(() => 
        {
            setIsLoading(false);
        });
    }, []);

    return(
        <AuthContext.Provider value={{authData, setAuthData, selectedGuild, setSelectedGuild, isLogged, setIsLogged, isLoading, setIsLoading}}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuthContext()
{
    const context = useContext(AuthContext);

    if(context === null)
    {
        throw new Error("useAuthContext must be used inside AuthProvider");
    }

    return context;
}