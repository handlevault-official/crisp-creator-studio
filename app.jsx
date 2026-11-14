import React from 'react';
import Logo from './Logo';

export default function Header() {
    return (
        <header className="bg-slate-900 border-b border-slate-800 py-4 px-6 flex items-center justify-between text-white">
            <div className="flex items-center gap-3">
                <Logo className="w-9 h-9" fill="#ef4444" icon="play" />
                <h1 className="text-xl font-bold tracking-wide">
                    Crisp Creator Studio
                </h1>
            </div>
        </header>
    );
}
