function varargout = GUI1(varargin)
% GUI1 MATLAB code for GUI1.fig
%      GUI1, by itself, creates a new GUI1 or raises the existing
%      singleton*.
%
%      H = GUI1 returns the handle to a new GUI1 or the handle to
%      the existing singleton*.
%
%      GUI1('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI1.M with the given input arguments.
%
%      GUI1('Property','Value',...) creates a new GUI1 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before GUI1_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to GUI1_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help GUI1

% Last Modified by GUIDE v2.5 14-Aug-2019 09:04:33

% Begin initialization code - DO NOT EDIT

gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @GUI1_OpeningFcn, ...
                   'gui_OutputFcn',  @GUI1_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before GUI1 is made visible.
function GUI1_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to GUI1 (see VARARGIN)

% Choose default command line output for GUI1
handles.output = hObject;
% Update handles structure
guidata(hObject, handles);

% UIWAIT makes GUI1 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = GUI1_OutputFcn(hObject, eventdata, handles) 

% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
set(handles.nepoch,'string',0);
varargout{1} = handles.output;


% --- Executes on button press in prev_epoch.
function prev_epoch_Callback(hObject, eventdata, handles)
    
% hObject    handle to prev_epoch (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    val = str2num(get(handles.nepoch,'string'));
    data = load('./check/BCICIV_calib_ds1a.mat');
    cnt = data.cnt;    
    erp = data.mrk.pos;
    if val > 1
    set(handles.nepoch,'string',val-1);
    n = erp(val-1);
    
    per_epoch = 700;
    Fs = 100;
    L = length(cnt(:,1));
    cnt = 0.1*double(cnt);
    ch1 = cnt(:,1);
    ch1 = ch1 - mean(ch1);
    ch2 = cnt(:,2);
    ch2 = ch2 - mean(ch2);
    ch3 = cnt(:,3);
    ch3 = ch3 - mean(ch3);
    ch4 = cnt(:,4);
    ch4 = ch4 - mean(ch4);
    ch5 = cnt(:,5);
    ch5 = ch5 - mean(ch5);
    ch6 = cnt(:,52);
    ch6 = ch6 - mean(ch6);
    
    begining = (n)- per_epoch/2;
    ending = (n)+per_epoch/2;
    if  ending <= L &&  begining>0 
    data = ch1(begining:ending,1);
    axes(handles.t1);
    plot(data)
    data = ch2(begining:ending,1);
    axes(handles.t2);
    plot(data)
    data = ch3(begining:ending,1);
    axes(handles.t3);
    plot(data)
    data = ch4(begining:ending,1);
    axes(handles.t4);
    plot(data)
    data = ch5(begining:ending,1);
    axes(handles.t5);
    plot(data)
    data = ch6(begining:ending,1);
    axes(handles.t6);
    plot(data)
    end
 end
   


% --- Executes on button press in next_epoc.
function next_epoc_Callback(hObject, eventdata, handles)
% hObject    handle to next_epoc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    val = str2num(get(handles.nepoch,'string'));  
    set(handles.nepoch,'string',val+1);
    
    data = load('./check/BCICIV_calib_ds1a.mat');
    cnt = data.cnt;
    erp = data.mrk.pos;
    n = erp(val+1);
    per_epoch = 700;
    Fs = 100;
    L = length(cnt(:,1));
    cnt = 0.1*double(cnt);
    ch1 = cnt(:,1);
    ch1 = ch1 - mean(ch1);
    ch2 = cnt(:,2);
    ch2 = ch2 - mean(ch2);
    ch3 = cnt(:,3);
    ch3 = ch3 - mean(ch3);
    ch4 = cnt(:,4);
    ch4 = ch4 - mean(ch4);
    ch5 = cnt(:,5);
    ch5 = ch5 - mean(ch5);
    ch6 = cnt(:,52);
    ch6 = ch6 - mean(ch6);
    
    begining = (n)- per_epoch/2;
    ending = (n)+per_epoch/2;
    if  ending <= L &&  begining>0 
    data = ch1(begining:ending,1);
    axes(handles.t1);
    plot(data)
    data = ch2(begining:ending,1);
    axes(handles.t2);
    plot(data)
    data = ch3(begining:ending,1);
    axes(handles.t3);
    plot(data)
    data = ch4(begining:ending,1);
    axes(handles.t4);
    plot(data)
    data = ch5(begining:ending,1);
    axes(handles.t5);
    plot(data)
    data = ch6(begining:ending,1);
    axes(handles.t6);
    plot(data)
    end
   
        

function nepoch_Callback(hObject, eventdata, handles)
% hObject    handle to nepoch (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of nepoch as text
%        str2double(get(hObject,'String')) returns contents of nepoch as a double


% --- Executes during object creation, after setting all properties.
function nepoch_CreateFcn(hObject, eventdata, handles)
% hObject    handle to nepoch (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
