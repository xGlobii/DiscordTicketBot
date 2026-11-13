import { useEffect, useRef } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuthContext } from "../components/AuthContext";
import { Spinner } from "../components/Spinner";

export function Callback()
{
    const [searchParams] = useSearchParams();
    const code = searchParams.get("code");
    const effectRan = useRef(false);
    const navigate = useNavigate();

    const { setAuthData, setIsLogged } = useAuthContext();

    useEffect(() =>
    {
        if(!code || effectRan.current)
            return;

        effectRan.current = true;

        fetch(`https://localhost:7219/api/v1/auth/callback?code=${code}`, {method: "GET", headers: {"Content-Type": "application/json"}, credentials: "include"})
        .then((result) => 
        {
            if(result.ok)
                return result.json()
        })
        .then((data) => 
        {
            setAuthData(data);
            setIsLogged(true);
            navigate("/dashboard");
        });
    }, [code]);

    return(
        <>
            <Spinner loadingMessage="Redirecting..."/>
        </>
    );
}