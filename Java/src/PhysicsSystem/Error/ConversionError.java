package PhysicsSystem.Error;

public class ConversionError extends Throwable {
	public ConversionError() {
		super();
	}

	public ConversionError(String message) {
		super(message);
	}

	public ConversionError(String message, Throwable cause) {
		super(message, cause);
	}

	public ConversionError(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
		super(message, cause, enableSuppression, writableStackTrace);
	}

	public ConversionError(Throwable cause) {
		super(cause);
	}
}