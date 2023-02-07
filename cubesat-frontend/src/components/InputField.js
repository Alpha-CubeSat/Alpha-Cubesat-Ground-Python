import Form from 'react-bootstrap/Form';

export default function InputField(
    { name, label, type, placeholder, error, fieldRef, className }
) {
    return (
        <Form.Group controlId={name} className={className}>
            {label && <Form.Label>{label}</Form.Label>}
            <Form.Control
                type={type || 'text'}
                placeholder={placeholder}
                className={error && 'is-invalid'}
                ref={fieldRef}
            />
            <Form.Text className='text-danger'>{error}</Form.Text>
        </Form.Group>
    );
}
