function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%
    c_vec = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30] ;
sigma_vec = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30] ;
J_error = zeros(length(c_vec), length(sigma_vec) ) ;
for c_index = 1 :length(c_vec)
    for sigma_index = 1:length(sigma_vec)
        fprintf('finding optimum values for C,sigma');
        fprintf('Iteration %d \n', c_index * sigma_index);
        C     =    c_vec(c_index) ;
        sigma = sigma_vec(sigma_index) ;
        model= svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
        predictions = svmPredict(model, Xval);
        J_error(c_index, sigma_index) = mean(double(predictions ~= yval)) ;
    end
end

[row,col]=find(J_error == min(J_error(:))) ;
C = c_vec(row) ;
sigma = sigma_vec(col);


% =========================================================================

end
