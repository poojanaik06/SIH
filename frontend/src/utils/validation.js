// Email validation function
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Password validation function
export const validatePassword = (password) => {
  return password.length >= 6;
};

// Check if user is already registered
export const isUserRegistered = (email) => {
  const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
  return registeredUsers.some(user => user.email === email);
};

// Validate user credentials
export const validateUserCredentials = (email, password) => {
  const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
  return registeredUsers.find(user => user.email === email && user.password === password);
};

// Form validation for login with registration check
export const validateLoginForm = (email, password) => {
  const errors = {};
  
  if (!email) {
    errors.email = "Email is required";
  } else if (!validateEmail(email)) {
    errors.email = "Please enter a valid email address";
  } else if (!isUserRegistered(email)) {
    errors.email = "No account found with this email. Please sign up first.";
  }
  
  if (!password) {
    errors.password = "Password is required";
  } else if (!validatePassword(password)) {
    errors.password = "Password must be at least 6 characters long";
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

// Form validation for signup
export const validateSignupForm = (formData) => {
  const errors = {};
  
  if (!formData.firstName.trim()) {
    errors.firstName = "First name is required";
  }
  
  if (!formData.lastName.trim()) {
    errors.lastName = "Last name is required";
  }
  
  if (!formData.email) {
    errors.email = "Email is required";
  } else if (!validateEmail(formData.email)) {
    errors.email = "Please enter a valid email address";
  }
  
  if (!formData.password) {
    errors.password = "Password is required";
  } else if (!validatePassword(formData.password)) {
    errors.password = "Password must be at least 6 characters long";
  }
  
  if (!formData.farmSize) {
    errors.farmSize = "Please select your farm size";
  }
  
  if (!formData.agreeToTerms) {
    errors.agreeToTerms = "You must agree to the terms and conditions";
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};