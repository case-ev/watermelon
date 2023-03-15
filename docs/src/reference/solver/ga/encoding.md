# Encoding

Since there are two problems to solve, each one requires a different encoding scheme. For this reason, we will separate between the coding scheme for the graph and for the agent decisions.

Encoders are represented by the \\(\Phi\\) operator, indexed with the context in which it is used, while the decoder is simply the inverse of said encoder.

## CLP encoding

For the CLP, since \\(\mathbf{x}\\) is a vector of 0's and 1's, the trivial encoding would be to flatten it into a string. Thus, the encoding function \\(\Phi_{\mathbf{x}}: \\{0, 1\\}^{|V|}\rightarrow \mathbb{B}_{|V|}\\) is given by

\\[
    \Phi_{\mathbf{x}}(\mathbf{x}) = x_1x_2\dots x_{|V|}
\\]

Having the encoder, the decoder is trivial to obtain, and is given by

\\[
    \Phi_{\mathbf{x}}^{-1}\left(x_1x_2\dots x_{|V|}\right) = \left(\begin{matrix}
        x_1 \\\\
        x_2 \\\\
        \vdots \\\\
        x_{|V|}
    \end{matrix}\right)
\\]

## ARP encoding

While the encoding scheme for the CLP is trivial, the one used for the ARP is much more difficult to obtain.
