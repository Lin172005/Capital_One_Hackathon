# Namma Uzhavan Nanban - UI Frontend

A modern, responsive web interface for the AI-powered agricultural assistant that helps farmers with rice farming queries and disease diagnosis.

## Features

### 🤖 **Unified AI Query Assistant**
- **Smart Mode Selection**: Automatically detects connectivity and chooses the best AI model
- **Online Mode**: Uses Google Gemini AI for enhanced responses when internet is available
- **Offline Mode**: Seamlessly falls back to local Phi-3 model when offline
- **Automatic Fallback**: If online query fails, automatically tries offline mode
- **Real-time Status**: Bottom-right indicator shows current connectivity and AI model

### 📸 **Image Disease Diagnosis**
- Upload images of rice crops
- AI-powered disease identification using Gemini Vision
- Treatment recommendations in Tamil
- Drag & drop support

## UI Features

- **Modern Design**: Clean, professional interface with gradient backgrounds
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Tab Navigation**: Easy switching between text queries and image diagnosis
- **Real-time Feedback**: Loading states and response areas
- **Accessibility**: Keyboard shortcuts (Ctrl+Enter) and screen reader friendly
- **Multilingual Support**: Tamil and English interface elements
- **Smart Connectivity**: Automatic detection and model selection
- **Status Indicator**: Always visible connectivity and AI model information

## How It Works

1. **Connectivity Detection**: The system automatically checks if you're online
2. **Model Selection**: 
   - **Online**: Uses Google Gemini AI for best performance
   - **Offline**: Uses local Phi-3 model for reliable responses
3. **Automatic Fallback**: If online fails, automatically switches to offline mode
4. **Status Display**: Bottom-right corner shows current mode and AI model

## Quick Start

1. **Ensure the backend is running**:
   ```bash
   cd Capital_One_Hackathon
   python main.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

3. **Start using the application**:
   - The system automatically detects your connectivity
   - Ask questions in Tamil or English
   - Upload images for disease diagnosis
   - Check the bottom-right indicator for current mode

## File Structure

```
frontend/
├── index.html          # Main HTML file with unified interface
├── static/
│   ├── styles.css      # Modern CSS styling with status indicator
│   └── script.js       # Smart connectivity detection and unified handling
```

## API Endpoints Used

- `POST /api/text-query` - Online queries with Gemini AI
- `POST /api/offline-query` - Offline queries with Phi-3 (local)
- `POST /api/image-diagnosis` - Image-based disease diagnosis

## Status Indicator

The bottom-right status indicator shows:
- **🟢 Online - Using Gemini AI**: When connected to internet
- **🟡 Offline - Using Phi-3 (Local)**: When offline or using local model
- **🔵 Checking connectivity...**: During connectivity checks

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Responsive Breakpoints

- **Desktop**: 1200px and above
- **Tablet**: 768px - 1199px
- **Mobile**: 480px - 767px
- **Small Mobile**: Below 480px

## Keyboard Shortcuts

- `Ctrl + Enter`: Submit text queries quickly
- `Tab`: Navigate between form elements
- `Enter`: Submit forms

## Smart Features

- **Automatic Connectivity Detection**: No manual mode switching needed
- **Intelligent Fallback**: Seamless transition between online/offline modes
- **Periodic Health Checks**: Monitors connectivity every 30 seconds
- **Real-time Status Updates**: Always know which AI model is being used

## Customization

The UI can be easily customized by modifying:

- **Colors**: Update CSS variables in `styles.css`
- **Fonts**: Change font families in the CSS
- **Layout**: Modify grid and flexbox properties
- **Animations**: Adjust transition timings and effects
- **Status Indicator**: Customize position, colors, and animations

## Troubleshooting

### Frontend not loading?
- Ensure the backend server is running
- Check that `frontend/` directory exists in the project root
- Verify file permissions

### Images not uploading?
- Check file format (JPG, PNG, JPEG supported)
- Ensure file size is reasonable (< 10MB recommended)
- Check browser console for errors

### API calls failing?
- Verify backend server is running on correct port
- Check network connectivity
- Review browser console for error messages
- The system will automatically try offline mode as fallback

### Status indicator not updating?
- Check browser console for connectivity check errors
- Ensure the page has internet access for initial connectivity test
- Refresh the page to reinitialize connectivity detection

## Development

To modify the frontend:

1. Edit the HTML structure in `index.html`
2. Update styles in `styles.css`
3. Modify functionality in `script.js`
4. Refresh the browser to see changes

## Dependencies

- **Font Awesome 6.0**: For icons
- **Google Fonts (Inter)**: For typography
- **Vanilla JavaScript**: No external JS frameworks required

## License

This frontend is part of the Namma Uzhavan Nanban project - Our Farmer's Friend.
