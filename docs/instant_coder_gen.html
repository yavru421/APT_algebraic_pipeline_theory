import { useState, useEffect, Fragment } from 'react';

// Define types for the configuration and variables
interface WizardConfig {
llmKey: string;
llmEndpoint: string;
country: string;
name: string;
modelPreference: string;
pythonPath: string;
powershellPath: string;
ffmpegPath: string;
dockerEnabled: boolean;
persistencePath: string;
tempPath: string;
}

interface Variable {
id: string;
name: string;
type: string; // e.g., 'string', 'number', 'array', 'object', 'file'
valuePreview: string; // A short string representation
metadata: Record<string, string>;
    snapshots: string[]; // Dates/timestamps of snapshots
    description: string;
    }

    const AlgebraicRuntimeOS = () => {
    const [currentWizardStep, setCurrentWizardStep] = useState<number>(0);
        const [isSetupComplete, setIsSetupComplete] = useState<boolean>(false);
            const [wizardConfig, setWizardConfig] = useState<WizardConfig>({
                llmKey: '',
                llmEndpoint: 'https://api.openai.com/v1',
                country: 'USA',
                name: 'Default User',
                modelPreference: 'gpt-4o',
                pythonPath: '/usr/bin/python3',
                powershellPath: '/usr/bin/pwsh',
                ffmpegPath: '/usr/bin/ffmpeg',
                dockerEnabled: true,
                persistencePath: '/home/user/algebraic_data/vars',
                tempPath: '/tmp/algebraic_temp',
                });

                const [equationInput, setEquationInput] = useState<string>(`// Define your algebraic workflows here
                    // Example:
                    // A = load_data('my_input.csv')
                    // B = process_data(A, 'clean_strategy_1')
                    // C = analyze_sentiment(B)
                    // D = generate_report(C, 'markdown')

                    // For AI tasks:
                    // E = llm_query("Summarize this document: {document_text}", document_text=load_file('doc.txt'))
                    // F = tts_convert(E, voice='alloy')
                    // G = ffmpeg_encode(F, 'output.mp3')

                    // Remember: Each variable can be a module, a result, or an intermediate state.
                    `);
                    const [executionLog, setExecutionLog] = useState<string>('');
                        const [variables, setVariables] = useState<Variable[]>([
                            {
                            id: 'var_input_data',
                            name: 'input_data',
                            type: 'file',
                            valuePreview: 'my_document.txt',
                            metadata: { source: 'user_upload', size: '1.2MB' },
                            snapshots: ['2023-10-26T10:00:00Z', '2023-10-26T10:30:00Z'],
                            description: 'Raw input document for processing.',
                            },
                            {
                            id: 'var_summary',
                            name: 'ai_summary',
                            type: 'string',
                            valuePreview: 'A concise summary of the document...',
                            metadata: { model: 'gpt-4o', token_cost: '0.05' },
                            snapshots: ['2023-10-26T11:00:00Z'],
                            description: 'AI-generated summary of the input_data.',
                            },
                            {
                            id: 'var_audio_output',
                            name: 'audio_output',
                            type: 'audio',
                            valuePreview: 'summary.mp3',
                            metadata: { voice: 'alloy', codec: 'mp3' },
                            snapshots: ['2023-10-26T11:15:00Z'],
                            description: 'Audio rendition of the AI summary.',
                            },
                            ]);
                            const [selectedVariableId, setSelectedVariableId] = useState<string | null>(null);

                                const totalWizardSteps = 5; // 0-indexed, so 5 steps means 0 to 4

                                const handleWizardChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>)
                                    => {
                                    const { name, value, type } = e.target;
                                    if (type === 'checkbox') {
                                    const checked = (e.target as HTMLInputElement).checked;
                                    setWizardConfig(prev => ({ ...prev, [name]: checked }));
                                    } else {
                                    setWizardConfig(prev => ({ ...prev, [name]: value }));
                                    }
                                    };

                                    const handleNextWizardStep = () => {
                                    if (currentWizardStep < totalWizardSteps - 1) { setCurrentWizardStep(prev=> prev +
                                        1);
                                        } else {
                                        setIsSetupComplete(true);
                                        setExecutionLog(`System initialized with the following
                                        configuration:\n${JSON.stringify(wizardConfig, null, 2)}\nReady to build
                                        workflows!`);
                                        }
                                        };

                                        const handleBackWizardStep = () => {
                                        if (currentWizardStep > 0) {
                                        setCurrentWizardStep(prev => prev - 1);
                                        }
                                        };

                                        const executeEquations = () => {
                                        setExecutionLog('Executing equations...\n');
                                        // Simulate execution
                                        setTimeout(() => {
                                        setExecutionLog(prev => prev + `Equations parsed and dependencies resolved.\n`);
                                        setExecutionLog(prev => prev + `Running 'load_data' for 'my_input.csv'...\n`);
                                        setExecutionLog(prev => prev + `Data loaded into variable A.\n`);
                                        setExecutionLog(prev => prev + `Processing data with 'clean_strategy_1'...\n`);
                                        setExecutionLog(prev => prev + `Variable B updated with processed data.\n`);
                                        setExecutionLog(prev => prev + `AI task 'summarize' initiated for variable
                                        E...\n`);
                                        setExecutionLog(prev => prev + `Output of E stored. Performing TTS conversion
                                        for F...\n`);
                                        setExecutionLog(prev => prev + `FFmpeg encoding G to 'output.mp3'...\n`);
                                        setExecutionLog(prev => prev + `Execution complete. Variables updated.\n`);

                                        // Simulate updating a variable
                                        setVariables(prev =>
                                        prev.map(v =>
                                        v.id === 'var_summary'
                                        ? { ...v, valuePreview: 'Detailed AI summary generated.', snapshots:
                                        [...v.snapshots, new Date().toISOString()] }
                                        : v
                                        )
                                        );
                                        }, 1500);
                                        };

                                        const addDummyVariable = () => {
                                        const newId = `var_${Math.random().toString(36).substr(2, 9)}`;
                                        const newVar: Variable = {
                                        id: newId,
                                        name: `new_variable_${variables.length + 1}`,
                                        type: 'string',
                                        valuePreview: 'Hello, world!',
                                        metadata: { created: new Date().toISOString() },
                                        snapshots: [new Date().toISOString()],
                                        description: 'A newly added variable for demonstration.',
                                        };
                                        setVariables(prev => [...prev, newVar]);
                                        };

                                        const selectedVariable = selectedVariableId
                                        ? variables.find(v => v.id === selectedVariableId)
                                        : null;

                                        const renderWizardStep = (step: number) => {
                                        switch (step) {
                                        case 0:
                                        return (
                                        <div className="text-center">
                                            <h2 className="text-3xl font-bold text-gray-800 mb-6">Welcome to the
                                                Algebraic Runtime Environment!</h2>
                                            <p className="text-lg text-gray-700 max-w-2xl mx-auto">
                                                This setup wizard will guide you through the initial configuration of
                                                your algebraic OS.
                                                Prepare your API keys, execution backend paths, and preferences.
                                            </p>
                                        </div>
                                        );
                                        case 1:
                                        return (
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                                            <div>
                                                <label htmlFor="llmKey"
                                                    className="block text-sm font-medium text-gray-700">
                                                    AI API Key (e.g., OpenAI)
                                                </label>
                                                <input type="password" name="llmKey" id="llmKey"
                                                    value={wizardConfig.llmKey} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx" />
                                            </div>
                                            <div>
                                                <label htmlFor="llmEndpoint"
                                                    className="block text-sm font-medium text-gray-700">
                                                    AI API Endpoint
                                                </label>
                                                <input type="text" name="llmEndpoint" id="llmEndpoint"
                                                    value={wizardConfig.llmEndpoint} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="https://api.openai.com/v1" />
                                            </div>
                                            <div>
                                                <label htmlFor="country"
                                                    className="block text-sm font-medium text-gray-700">
                                                    Country
                                                </label>
                                                <input type="text" name="country" id="country"
                                                    value={wizardConfig.country} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="USA" />
                                            </div>
                                            <div>
                                                <label htmlFor="name"
                                                    className="block text-sm font-medium text-gray-700">
                                                    User Name
                                                </label>
                                                <input type="text" name="name" id="name" value={wizardConfig.name}
                                                    onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="John Doe" />
                                            </div>
                                            <div className="col-span-full">
                                                <label htmlFor="modelPreference"
                                                    className="block text-sm font-medium text-gray-700">
                                                    Default AI Model Preference
                                                </label>
                                                <select name="modelPreference" id="modelPreference"
                                                    value={wizardConfig.modelPreference} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2">
                                                    <option value="gpt-4o">GPT-4o</option>
                                                    <option value="gpt-4-turbo">GPT-4 Turbo</option>
                                                    <option value="claude-3-opus">Claude 3 Opus</option>
                                                    <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                                                </select>
                                            </div>
                                        </div>
                                        );
                                        case 2:
                                        return (
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                                            <div>
                                                <label htmlFor="pythonPath"
                                                    className="block text-sm font-medium text-gray-700">
                                                    Python Executable Path
                                                </label>
                                                <input type="text" name="pythonPath" id="pythonPath"
                                                    value={wizardConfig.pythonPath} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="/usr/bin/python3" />
                                            </div>
                                            <div>
                                                <label htmlFor="powershellPath"
                                                    className="block text-sm font-medium text-gray-700">
                                                    PowerShell Core Executable Path
                                                </label>
                                                <input type="text" name="powershellPath" id="powershellPath"
                                                    value={wizardConfig.powershellPath} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="/usr/bin/pwsh" />
                                            </div>
                                            <div>
                                                <label htmlFor="ffmpegPath"
                                                    className="block text-sm font-medium text-gray-700">
                                                    FFmpeg Executable Path
                                                </label>
                                                <input type="text" name="ffmpegPath" id="ffmpegPath"
                                                    value={wizardConfig.ffmpegPath} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="/usr/bin/ffmpeg" />
                                            </div>
                                            <div className="flex items-center mt-6">
                                                <input id="dockerEnabled" name="dockerEnabled" type="checkbox"
                                                    checked={wizardConfig.dockerEnabled} onChange={handleWizardChange}
                                                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                                                <label htmlFor="dockerEnabled"
                                                    className="ml-2 block text-sm font-medium text-gray-700">
                                                    Enable Docker/CLI Tool Integration
                                                </label>
                                            </div>
                                        </div>
                                        );
                                        case 3:
                                        return (
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
                                            <div>
                                                <label htmlFor="persistencePath"
                                                    className="block text-sm font-medium text-gray-700">
                                                    Variable Persistence Folder
                                                </label>
                                                <input type="text" name="persistencePath" id="persistencePath"
                                                    value={wizardConfig.persistencePath} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="/home/user/algebraic_data/vars" />
                                                <p className="mt-1 text-xs text-gray-500">
                                                    Where all variable data, metadata, and snapshots will be stored.
                                                </p>
                                            </div>
                                            <div>
                                                <label htmlFor="tempPath"
                                                    className="block text-sm font-medium text-gray-700">
                                                    Temporary Files Folder
                                                </label>
                                                <input type="text" name="tempPath" id="tempPath"
                                                    value={wizardConfig.tempPath} onChange={handleWizardChange}
                                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-gray-50 text-gray-800 p-2"
                                                    placeholder="/tmp/algebraic_temp" />
                                                <p className="mt-1 text-xs text-gray-500">
                                                    For intermediate files and temporary outputs.
                                                </p>
                                            </div>
                                        </div>
                                        );
                                        case 4:
                                        return (
                                        <div
                                            className="max-w-2xl mx-auto bg-gray-50 p-6 rounded-lg border border-gray-200">
                                            <h3 className="text-xl font-semibold text-gray-800 mb-4">Review Your
                                                Configuration</h3>
                                            <pre
                                                className="bg-gray-100 p-4 rounded-md text-sm text-gray-700 whitespace-pre-wrap break-words overflow-auto h-64">
              {JSON.stringify(wizardConfig, null, 2)}
            </pre>
                                            <p className="mt-4 text-gray-700">
                                                Click 'Finish Setup' to complete the initial configuration and launch
                                                the Algebraic Interface.
                                            </p>
                                        </div>
                                        );
                                        default:
                                        return null;
                                        }
                                        };

                                        if (!isSetupComplete) {
                                        return (
                                        <div
                                            className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8 font-sans">
                                            <div
                                                className="bg-white shadow-xl rounded-xl p-10 w-full max-w-4xl border border-gray-200">
                                                <div className="flex justify-between items-center mb-8">
                                                    <h1 className="text-4xl font-extrabold text-blue-700">Algebraic OS
                                                        Setup</h1>
                                                    <div className="flex space-x-2">
                                                        {[...Array(totalWizardSteps)].map((_, index) => (
                                                        <div key={index} className={`w-6 h-6 rounded-full flex
                                                            items-center justify-center font-bold text-sm ${ index
                                                            <=currentWizardStep ? 'bg-blue-600 text-white'
                                                            : 'bg-gray-200 text-gray-600' }`}>
                                                            {index + 1}
                                                        </div>
                                                        ))}
                                                    </div>
                                                </div>

                                                <div className="min-h-80 flex items-center justify-center py-6">
                                                    {renderWizardStep(currentWizardStep)}
                                                </div>

                                                <div
                                                    className="flex justify-between mt-8 pt-4 border-t border-gray-200">
                                                    <button onClick={handleBackWizardStep}
                                                        disabled={currentWizardStep===0} className={`px-6 py-2
                                                        rounded-lg font-semibold transition duration-200 ${
                                                        currentWizardStep===0
                                                        ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
                                                        : 'bg-blue-100 text-blue-700 hover:bg-blue-200' }`}>
                                                        Back
                                                    </button>
                                                    <button onClick={handleNextWizardStep}
                                                        className="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 transition duration-200">
                                                        {currentWizardStep === totalWizardSteps - 1 ? 'Finish Setup' :
                                                        'Next'}
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                        );
                                        }

                                        // Algebraic Interface
                                        return (
                                        <div className="min-h-screen bg-gray-100 text-gray-800 flex flex-col font-sans">
                                            {/* Header */}
                                            <header
                                                className="bg-blue-700 text-white p-4 shadow-md flex justify-between items-center">
                                                <h1 className="text-2xl font-bold">Algebraic Runtime OS</h1>
                                                <div className="text-sm">
                                                    User: {wizardConfig.name} | Model: {wizardConfig.modelPreference}
                                                </div>
                                            </header>

                                            {/* Main Dual-Pane Layout */}
                                            <div className="flex flex-1 overflow-hidden p-4 space-x-4">
                                                {/* Left Pane: Equations & Execution Log */}
                                                <div
                                                    className="flex flex-col w-3/5 bg-white rounded-xl shadow-md border border-gray-200 p-6 space-y-4">
                                                    <h2 className="text-xl font-semibold text-gray-800">Algebraic
                                                        Equations & Workflow</h2>
                                                    <textarea
                                                        className="flex-1 w-full p-4 border border-gray-300 rounded-lg font-mono text-sm bg-gray-50 focus:ring-blue-500 focus:border-blue-500 resize-none"
                                                        value={equationInput} onChange={e=> setEquationInput(e.target.value)}
            placeholder="Enter your algebraic equations here..."
          ></textarea>
                                                    <div className="flex justify-between items-center">
                                                        <button onClick={executeEquations}
                                                            className="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition duration-200 shadow-md">
                                                            Execute Workflow
                                                        </button>
                                                        <div className="flex space-x-2 text-gray-600 text-sm">
                                                            <span>{`⚡ Ready`}</span>
                                                            <span>|</span>
                                                            <span>{`🧠 AI Assistant (Offline)`}</span>
                                                        </div>
                                                    </div>
                                                    <div className="border-t border-gray-300 pt-4 mt-4">
                                                        <h3 className="text-lg font-semibold text-gray-800 mb-2">
                                                            Execution Log</h3>
                                                        <pre
                                                            className="bg-gray-100 p-4 rounded-lg text-xs text-gray-700 overflow-auto h-40 border border-gray-200">
              {executionLog || 'No activity yet.'}
            </pre>
                                                    </div>
                                                </div>

                                                {/* Right Pane: Variable/Module Management */}
                                                <div
                                                    className="flex flex-col w-2/5 bg-white rounded-xl shadow-md border border-gray-200 p-6 space-y-4">
                                                    <h2 className="text-xl font-semibold text-gray-800">Variables &
                                                        Modules</h2>
                                                    <div
                                                        className="flex-1 flex flex-col border border-gray-300 rounded-lg overflow-hidden">
                                                        <div
                                                            className="flex-none bg-gray-50 px-4 py-2 border-b border-gray-300 flex justify-between items-center">
                                                            <span className="font-medium text-gray-700">Available
                                                                Variables ({variables.length})</span>
                                                            <button onClick={addDummyVariable}
                                                                className="px-4 py-1 bg-blue-500 text-white text-sm rounded-lg hover:bg-blue-600 transition duration-200">
                                                                + Add Module
                                                            </button>
                                                        </div>
                                                        <ul
                                                            className="flex-1 overflow-y-auto divide-y divide-gray-200 bg-gray-50">
                                                            {variables.map(variable => (
                                                            <li key={variable.id} onClick={()=>
                                                                setSelectedVariableId(variable.id)}
                                                                className={`p-3 cursor-pointer hover:bg-blue-50 flex
                                                                items-center space-x-3 transition duration-150 ${
                                                                selectedVariableId === variable.id ? 'bg-blue-100
                                                                border-l-4 border-blue-600' : ''
                                                                }`}
                                                                >
                                                                <div
                                                                    className="bg-gray-200 border-2 border-dashed rounded-md w-10 h-10 flex-shrink-0 flex items-center justify-center text-gray-600 text-sm">
                                                                    {variable.type === 'string' && 'Txt'}
                                                                    {variable.type === 'file' && 'File'}
                                                                    {variable.type === 'audio' && 'Aud'}
                                                                    {!['string', 'file',
                                                                    'audio'].includes(variable.type) && 'Var'}
                                                                </div>
                                                                <div className="flex-1">
                                                                    <p className="font-semibold text-gray-800">
                                                                        {variable.name}</p>
                                                                    <p className="text-sm text-gray-600 truncate">
                                                                        {variable.valuePreview}</p>
                                                                </div>
                                                                <span
                                                                    className="text-xs text-gray-500 bg-gray-200 rounded-full px-2 py-1">
                                                                    {variable.type}
                                                                </span>
                                                            </li>
                                                            ))}
                                                        </ul>
                                                    </div>

                                                    {/* Variable Details / Metadata */}
                                                    <div className="border-t border-gray-300 pt-4 mt-4">
                                                        <h3 className="text-lg font-semibold text-gray-800 mb-2">
                                                            Variable Details {selectedVariable ?
                                                            `(${selectedVariable.name})` : ''}
                                                        </h3>
                                                        {selectedVariable ? (
                                                        <div
                                                            className="bg-gray-100 p-4 rounded-lg text-sm border border-gray-200">
                                                            <p className="mb-2">
                                                                <span className="font-semibold text-gray-700">ID:</span>
                                                                {selectedVariable.id}
                                                            </p>
                                                            <p className="mb-2">
                                                                <span
                                                                    className="font-semibold text-gray-700">Type:</span>{'
                                                                '}
                                                                <span
                                                                    className="bg-blue-200 text-blue-800 px-2 py-1 rounded-full text-xs">
                                                                    {selectedVariable.type}
                                                                </span>
                                                            </p>
                                                            <p className="mb-2">
                                                                <span
                                                                    className="font-semibold text-gray-700">Description:</span>
                                                                {selectedVariable.description}
                                                            </p>
                                                            <p className="mb-2">
                                                                <span className="font-semibold text-gray-700">Current
                                                                    Value:</span>{' '}
                                                                {selectedVariable.valuePreview}
                                                            </p>
                                                            <div className="mt-3">
                                                                <span
                                                                    className="font-semibold text-gray-700">Metadata:</span>
                                                                <ul className="list-disc list-inside text-gray-600">
                                                                    {Object.entries(selectedVariable.metadata).map(([key,
                                                                    value]) => (
                                                                    <li key={key}>
                                                                        {key}: {value}
                                                                    </li>
                                                                    ))}
                                                                </ul>
                                                            </div>
                                                            <div className="mt-3">
                                                                <span className="font-semibold text-gray-700">Snapshots
                                                                    ({selectedVariable.snapshots.length}):</span>
                                                                <ul
                                                                    className="list-disc list-inside text-gray-600 text-xs">
                                                                    {selectedVariable.snapshots.map((snapshot, index) =>
                                                                    (
                                                                    <li key={index}>{new
                                                                        Date(snapshot).toLocaleString()}</li>
                                                                    ))}
                                                                </ul>
                                                            </div>
                                                        </div>
                                                        ) : (
                                                        <p className="text-gray-600">Select a variable to view its
                                                            details.</p>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>

                                            {/* Footer (optional) */}
                                            <footer
                                                className="bg-gray-800 text-gray-300 p-3 text-center text-sm shadow-inner mt-4">
                                                Algebraic Runtime OS - Orchestrating everything with elegance.
                                            </footer>
                                        </div>
                                        );
                                        };

                                        export default AlgebraicRuntimeOS;
                                        }