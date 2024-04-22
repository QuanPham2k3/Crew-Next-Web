'use client';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

interface Message {
    type: string; // 'user' or 'ai'
    content: string;
}

const STORAGE_KEY = 'chatHistory';
export const useChatWeb = () => {
    const [url, setUrl] = useState('');
    const [conversationHistory, setConversationHistory] = useState<Message[]>([]);
    const [userQuery, setUserQuery] = useState('');
    const [aiResponse, setAiResponse] = useState('');
    const [errors, setErrors] = useState<Record<string, string>>({});

    useEffect(() => {
        const storedHistory = localStorage.getItem(STORAGE_KEY);
        if (storedHistory) {
            try {
                const parsedHistory = JSON.parse(storedHistory);
                setConversationHistory(parsedHistory);
            } catch (error) {
                console.error('Error parsing stored conversation history:', error);
            }
        }
    }, []);
    
    useEffect(() => {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(conversationHistory));
    }, [conversationHistory]);

    const handleUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUrl(event.target.value);
    };

    const handleUserInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        const newQuery = event.target.value;
        setUserQuery(newQuery);

        // Validate userQuery on input change (basic validation)
        const updatedErrors = { ...errors };
        if (!newQuery.trim()) {
            updatedErrors.userQuery = 'Please enter a question.';
        } else {
            delete updatedErrors.userQuery;
        }

        setErrors(updatedErrors);
    };

    const handleSubmit = async (event: React.KeyboardEvent) => {
        if (event.key === 'Enter' && !Object.values(errors).length) {
            // Reset errors before API call
            setErrors({});
            console.log('Submitting question:', url, userQuery);

            try {
                const response = await axios.post('http://localhost:3001/api/answer_question', 
                    {
                        url,
                        userQuery,
                    });
                toast.success('Chat started');

                const { answer } = response.data;
                console.log('AI response:', answer);

                setConversationHistory((prevConversationHistory) => {
                    console.log('Previous conversation history:', prevConversationHistory); // Log previous state
                    const newConversationHistory = [
                        ...prevConversationHistory,
                        { type: 'user', content: userQuery },
                        { type: 'ai', content: answer },
                    ];
                    console.log('Updated conversation history:', newConversationHistory); // Log updated state
                    return newConversationHistory;
                });

                setUserQuery('');
                setAiResponse(answer);
            } catch (error) {
                console.error('Error submitting question:', error);
                setErrors({ apiError: 'An error occurred while communicating with the server.' });
                toast.error('Error submitting question');
            }
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
        errors,
    };
};
