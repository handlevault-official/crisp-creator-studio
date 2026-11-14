import React from 'react';

export default function Logo({ className = "w-8 h-8", fill = "#ef4444", icon = "play" }) {
    // Pwedeng magbago ng icon sa loob depende sa app (play para sa creator, doc para sa resume, atbp.)
    const renderIconPath = () => {
        if (icon === 'doc') {
            return <path d="M30 20 h40 v60 h-40 z M40 35 h20 M40 50 h20" stroke="white" strokeWidth="6" fill="none" strokeLinecap="round" />;
        }
        // Default: Play / YouTube / Creator triangle
        return <polygon points="40,30 72,50 40,70" fill="white" />;
    };

    return (
        <svg className={`inline-block shrink-0 ${className}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <rect width="100" height="100" rx="25" fill={fill} />
            {renderIconPath()}
        </svg>
    );
}
