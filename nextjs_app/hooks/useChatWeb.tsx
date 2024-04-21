
"use client";

import React, { useState, useEffect } from 'react';
import axios from "axios";
import toast from 'react-hot-toast';

export const useChatWeb = () => {
    const [url, setUrl] = useState(''); // Removed vector store
    const [conversationHistory, setConversationHistory] = useState<{ type: string; content: string }[]>([]);
    const [userQuery, setUserQuery] = useState('');
    const [aiResponse, setAiResponse] = useState('');

    const handleUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUrl(event.target.value);
    };

    const handleUserInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setUserQuery(event.target.value);
    }; 
    
    const handleSubmit = async () => {
        if (!userQuery) {
            return;
        }
    
        try {
            const response = await axios.post(
                'http://localhost:3001/api/answer_question', 
                {
                    url,
                    userQuery,
                }
            );
            toast.success("Chat started");

            const { answer } = response.data;
            console.log('AI response:', answer);
            
            setAiResponse(answer);
            setConversationHistory([...conversationHistory, { type: 'user', content: userQuery }, { type: 'ai', content: answer }]);
            setUserQuery('');
        } catch (error) {
            console.error('Error submitting question:', error);
            toast.error('Error submitting question');
        }
    };  
    
    return {
        url,
        setUrl,
        conversationHistory,
        userQuery,
        setUserQuery,
        handleUserInput,
        handleSubmit,
        aiResponse,
      };
    };
    

