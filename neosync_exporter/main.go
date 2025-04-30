package main

import (
	"C"
	"fmt"

	mgmtv1alpha1 "github.com/nucleuscloud/neosync/backend/gen/go/protos/mgmt/v1alpha1"
	"github.com/nucleuscloud/neosync/worker/pkg/benthos/transformer_executor"
)

var transformerExecutors = map[string]*transformer_executor.TransformerExecutor{}

//export Mutate
func Mutate(jsCode *C.char, value *C.char) (*C.char, *C.char) {
	jsCodeStr := C.GoString(jsCode)

	if _, ok := transformerExecutors[jsCodeStr]; !ok {
		executor, err := transformer_executor.InitializeTransformerByConfigType(
			&mgmtv1alpha1.TransformerConfig{
				Config: &mgmtv1alpha1.TransformerConfig_TransformJavascriptConfig{
					TransformJavascriptConfig: &mgmtv1alpha1.TransformJavascript{Code: jsCodeStr},
				},
			},
		)
		if err != nil {
			return nil, C.CString("failed to initialize transformer")
		}

		transformerExecutors[jsCodeStr] = executor
	}

	result, err := transformerExecutors[jsCodeStr].Mutate(C.GoString(value), nil)
	if err != nil {
		return nil, C.CString("failed to run transformer")
	}

	if result == nil {
		return nil, nil
	}

	switch v := result.(type) {
	case string:
		return C.CString(v), nil
	case *string:
		return C.CString(*v), nil
	default:
		return nil, C.CString(fmt.Sprintf("unexpected transformer result type: %T, value=%v", result, result))
	}
}

func main() {}
