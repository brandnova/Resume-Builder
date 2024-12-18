const PDFGenerator = () => {
    const [status, setStatus] = React.useState('preparing');
    
    React.useEffect(() => {
        if (window.resumeData.paymentVerified) {
            generatePDF();
        }
    }, []);

    const generatePDF = async () => {
        try {
            setStatus('generating');
            const content = document.getElementById('resume-content').cloneNode(true);
            content.style.display = 'block';
            
            const options = {
                margin: 0,
                filename: `${window.resumeData.title}.pdf`,
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { 
                    scale: 2,
                    useCORS: true,
                    logging: false
                },
                jsPDF: { 
                    unit: 'in', 
                    format: 'letter', 
                    orientation: 'portrait'
                }
            };

            await html2pdf().set(options).from(content).save();
            setStatus('completed');
            
            // Redirect back to preview after short delay
            setTimeout(() => {
                window.location.href = `/resumes/${window.resumeData.slug}/preview/`;
            }, 2000);

        } catch (error) {
            console.error('PDF generation failed:', error);
            setStatus('error');
        }
    };

    const statusMessages = {
        preparing: 'Preparing your PDF...',
        generating: 'Generating your PDF...',
        completed: 'PDF generated successfully! Redirecting...',
        error: 'An error occurred. Please try again.'
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-xl max-w-md w-full mx-4">
                <div className="text-center">
                    <div className="mb-4">
                        {status === 'generating' && (
                            <svg className="animate-spin h-8 w-8 mx-auto text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        )}
                        {status === 'completed' && (
                            <svg className="h-8 w-8 mx-auto text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        )}
                        {status === 'error' && (
                            <svg className="h-8 w-8 mx-auto text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        )}
                    </div>
                    <p className="text-lg font-medium text-gray-900">
                        {statusMessages[status]}
                    </p>
                </div>
            </div>
        </div>
    );
};

// Mount component
const mountPoint = document.getElementById('pdf-generator');
if (mountPoint) {
    ReactDOM.render(<PDFGenerator />, mountPoint);
}
