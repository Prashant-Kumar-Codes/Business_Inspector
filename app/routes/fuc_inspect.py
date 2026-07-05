import io
import base64

# Helper function to convert a matplotlib figure to base64
def fig_to_base64(fig):
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png', bbox_inches='tight')
    img_buf.seek(0)
    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    return img_base64